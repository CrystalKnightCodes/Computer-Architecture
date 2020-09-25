import sys

"""
----------------------
OPERATION CODES
----------------------
"""
operation_codes = {
'NOP'  : 0b00000000,
'HLT'  : 0b00000001,
'ST'   : 0b10000100,
'LD'   : 0b10000011,
'LDI'  : 0b10000010,
'JMP'  : 0b01010100,
'JEQ'  : 0b01010101,
'JNE'  : 0b01010110,
'JLT'  : 0b01011000,
'JLE'  : 0b01011001,
'JGT'  : 0b01010111,
'JGE'  : 0b01011010,
'PRA'  : 0b01001000,
'PRN'  : 0b01000111,
'CMP'  : 0b10100111,
'ADD'  : 0b10100000,
'ADDI' : 0b10100101,
'INC'  : 0b01100101,
'SUB'  : 0b10100001,
'SUBI' : 0b10101110,
'DEC'  : 0b01100110,
'MUL'  : 0b10100010,
'DIV'  : 0b10100011,
'MOD'  : 0b10100100,
'SHL'  : 0b10101100,
'SHR'  : 0b10101101,
'AND'  : 0b10101000,
'OR'   : 0b10101010,
'NOT'  : 0b01101001,
'XOR'  : 0b10101011
}

"""
END OPERATION CODES
--
BEGIN OPERATION CODE INSTRUCTIONS
""" 

class Instructions():
    def __init__(self, cpu):
        self.cpu = cpu

    """
    Basic
    """
    # NOP
    # No operation. Do nothing for this instruction.
    # Machine code:
    # 00000000
    # 00
    NOP         = 0b00000000
    def handle_NOP(self):
        print("NOP Encountered. Skipping...")

    # HLT
    # Halt the CPU (and exit the emulator).
    # Machine code:
    # 00000001 
    # 01
    HLT         = 0b00000001
    def handle_HLT(self):
        sys.exit("HALT called! Exiting...")


    """
    Memory Read/Write
    """
    # ST registerA registerB
    # Store value in registerB in the address stored in registerA.
    # This opcode writes to memory.
    # Machine code:
    # 10000100 00000aaa 00000bbb
    # 84 0a 0b
    ST          = 0b10000100
    def handle_ST(self, r1, r2):
        self.cpu.ram_write(self.cpu.reg[r1], self.cpu.reg[r2])

    # LD registerA registerB
    # Loads registerA with the value at the memory address stored in registerB.
    # This opcode reads from memory.
    # Machine code:
    # 10000011 00000aaa 00000bbb
    # 83 0a 0b
    LD          = 0b10000011
    def handle_LD(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.ram_read(self.cpu.reg[r2])

    # LDI register immediate
    # Set the value of a register to an integer.
    # Machine code:
    # 10000010 00000rrr iiiiiiii
    # 82 0r ii
    LDI         = 0b10000010
    def handle_LDI(self, r1, r2):
        self.cpu.reg[r1] = r2


    """
    Jump & Conditional Jump
    """
    # JMP register
    # Jump to the address stored in the given register.
    # Set the PC to the address stored in the given register.
    # Machine code:
    # 01010100 00000rrr
    # 54 0r
    JMP         = 0b01010100
    def handle_JMP(self, r1):
        self.cpu.pc = self.cpu.reg[r1]

    # JEQ register
    # If equal flag is set (true), jump to the address stored in the given register.
    # Machine code:
    # 01010101 00000rrr
    # 55 0r
    JEQ         = 0b01010101
    def handle_JEQ(self, r1):
        if (self.cpu.fl & 0b00000001):
            self.cpu.pc = self.cpu.reg[r1]
        else:
            self.cpu.pc = (self.cpu.pc + 2) & 0xff

    # JNE register
    # If E flag is clear (false, 0), jump to the address stored in the given register.
    # Machine code:
    # 01010110 00000rrr
    # 56 0r
    JNE         = 0b01010110
    def handle_JNE(self, r1):
        if (self.cpu.fl & 0b00000001):
            self.cpu.pc = (self.cpu.pc + 2) & 0xff
        else:
            self.cpu.pc = self.cpu.reg[r1]

    # JLT register
    # If less-than flag is set (true), jump to the address stored in the given register.
    # Machine code:
    # 01011000 00000rrr
    # 58 0r
    JLT         = 0b01011000
    def handle_JLT(self, r1):
        if (self.cpu.fl & 0b00000100):
            self.cpu.pc = self.cpu.reg[r1]
        else:
            self.cpu.pc = (self.cpu.pc + 2) & 0xff

    # JLE register
    # If less-than flag or equal flag is set (true), jump to the address stored in the given register.
    # 01011001 00000rrr
    # 59 0r
    JLE         = 0b01011001
    def handle_JLE(self, r1):
        if (self.cpu.fl & 0b00000101):
            self.cpu.pc = self.cpu.reg[r1]
        else:
            self.cpu.pc = (self.cpu.pc + 2) & 0xff

    # JGT register
    # If greater-than flag is set (true), jump to the address stored in the given register.
    # Machine code:
    # 01010111 00000rrr
    # 57 0r
    JGT         = 0b01010111
    def handle_JGT(self, r1):
        if (self.cpu.fl & 0b00000010):
            self.cpu.pc = self.cpu.reg[r1]
        else:
            self.cpu.pc = (self.cpu.pc + 2) & 0xff            

    # JGE register
    # If greater-than flag or equal flag is set (true), jump to the address stored in the given register.
    # 01011010 00000rrr
    # 5A 0r
    JGE         = 0b01011010
    def handle_JGE(self, r1):
        if (self.cpu.fl & 0b00000011):
            self.cpu.pc = self.cpu.reg[r1]
        else:
            self.cpu.pc = (self.cpu.pc + 2) & 0xff


    """
    I/O Instructions
    """
    # PRA register pseudo-instruction
    # Print alpha character value stored in the given register.
    # Print to the console the ASCII character corresponding to the value in the register.
    # Machine code:
    # 01001000 00000rrr
    # 48 0r
    PRA         = 0b01001000
    def handle_PRA(self, r1):
        print(chr(self.cpu.reg[r1]))

    # PRN register pseudo-instruction
    # Print numeric value stored in the given register.
    # Print to the console the decimal integer value that is stored in the given register.
    # Machine code:
    # 01000111 00000rrr
    # 47 0r
    PRN         = 0b01000111
    def handle_PRN(self, r1):
        print(self.cpu.reg[r1])


    """
    ALU Instructions
    """
    # CMP registerA registerB
    # Compare the values in two registers.
    # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
    # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
    # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
    # Machine code:
    # 10100111 00000aaa 00000bbb
    # A7 0a 0b
    CMP         = 0b10100111
    def handle_CMP(self, r1, r2):
        self.cpu.fl = self.cpu.fl & 0b00000000
        item1 = self.cpu.reg[r1]
        item2 = self.cpu.reg[r2]

        if item1 < item2:
            self.cpu.fl = self.cpu.fl | 0b00000100
        elif item1 > item2:
            self.cpu.fl = self.cpu.fl | 0b00000010
        else:
            self.cpu.fl = self.cpu.fl | 0b00000001

    # ADD registerA registerB
    # Add the value in two registers and store the result in registerA.
    # Machine code:
    # 10100000 00000aaa 00000bbb
    # A0 0a 0b
    ADD         = 0b10100000
    def handle_ADD(self, r1, r2):
        self.cpu.reg[r1] = (self.cpu.reg[r1] + self.cpu.reg[r2]) & 0xff

    # ADDI register immediate
    # Add an immediate value to the register.
    # Machine code:
    # 10100101 00000rrr iiiiiiii
    # A5 0r ii
    ADDI        = 0b10100101
    def handle_ADDI(self, r1, val):
        self.cpu.reg[r1] = (self.cpu.reg[r1] + val) & 0xff

    # INC register
    # Increment (add 1 to) the value in the given register.
    # Machine code:
    # 01100101 00000rrr
    # 65 0r
    INC         = 0b01100101
    def handle_INC(self, r1):
        self.cpu.reg[r1] = (self.cpu.reg[r1] + 1) & 0xff

    # SUB registerA registerB
    # Subtract the value in the second register from the first, storing the result in registerA.
    # Machine code:
    # 10100001 00000aaa 00000bbb
    # A1 0a 0b
    SUB         = 0b10100001
    def handle_SUB(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] - self.cpu.reg[r2]

    # SUBI register immediate
    # Subtract an immediate value from the register.
    # Machine code:
    # 10101110 00000rrr iiiiiiii
    # AE 0r ii
    SUBI        = 0b10101110
    def handle_SUBI(self, r1, val):
        self.cpu.reg[r1] = (self.cpu.reg[r1] - val) & 0xff

    # DEC register
    # Decrement (subtract 1 from) the value in the given register.
    # Machine code:
    # 01100110 00000rrr
    # 66 0r
    DEC         = 0b01100110
    def handle_DEC(self, r1):
        self.cpu.reg[r1] = (self.cpu.reg[r1] - 1) & 0xff

    # MUL registerA registerB
    # Multiply the values in two registers together and store the result in registerA.
    # Machine code:
    # 10100010 00000aaa 00000bbb
    # A2 0a 0b
    MUL         = 0b10100010
    def handle_MUL(self, r1, r2):
        self.cpu.reg[r1] = (self.cpu.reg[r1] * self.cpu.reg[r2]) & 0xff

    # DIV registerA registerB
    # Divide the value in the first register by the value in the second, storing the result in registerA.
    # If the value in the second register is 0, the system should print an error message and halt.
    # Machine code:
    # 10100011 00000aaa 00000bbb
    # A3 0a 0b
    DIV         = 0b10100011
    def handle_DIV(self, r1, r2):
        self.cpu.reg[r1] = (self.cpu.reg[r1] // self.cpu.reg[r2]) & 0xff        

    # MOD registerA registerB
    # Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.
    # If the value in the second register is 0, the system should print an error message and halt.
    # Machine code:
    # 10100100 00000aaa 00000bbb
    # A4 0a 0b
    MOD         = 0b10100100
    def handle_MOD(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] % self.cpu.reg[r2]

    # Shift the value in registerA left by the number of bits specified in registerB, filling the low bits with 0.
    # 10101100 00000aaa 00000bbb
    # AC 0a 0b
    SHL         = 0b10101100
    def handle_SHL(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] << self.cpu.reg[r2]

    # Shift the value in registerA right by the number of bits specified in registerB, filling the high bits with 0.
    # 10101101 00000aaa 00000bbb
    # AD 0a 0b
    SHR         = 0b10101101
    def handle_SHR(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] >> self.cpu.reg[r2]

    # AND registerA registerB
    # Bitwise-AND the values in registerA and registerB, then store the result in registerA.
    # Machine code:
    # 10101000 00000aaa 00000bbb
    # A8 0a 0b
    AND         = 0b10101000
    def handle_AND(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] & self.cpu.reg[r2]

    # OR registerA registerB
    # Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA.
    # Machine code:
    # 10101010 00000aaa 00000bbb
    # AA 0a 0b
    OR          = 0b10101010
    def handle_OR(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] | self.cpu.reg[r2]

    # NOT register
    # Perform a bitwise-NOT on the value in a register, storing the result in the register.
    # Machine code:
    # 01101001 00000rrr
    # 69 0r
    NOT         = 0b01101001
    def handle_NOT(self, r1):
        self.cpu.reg[r1] = ~self.cpu.reg[r1]

    # XOR registerA registerB
    # Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA.
    # Machine code:
    # 10101011 00000aaa 00000bbb
    # AB 0a 0b
    XOR         = 0b10101011
    def handle_XOR(self, r1, r2):
        self.cpu.reg[r1] = self.cpu.reg[r1] ^ self.cpu.reg[r2]

"""
END INSTRUCTIONS
"""