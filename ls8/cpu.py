"""CPU functionality."""

import sys
from operations import *

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Internal Registers
        self.pc     = 0b00000000
        self.ir     = operation_codes['NOP']
        self.mar    = 0b00000000
        self.mdr    = 0b00000000
        self.fl     = 0b00000000  # 00000LGE - only last 3 bits matter

        # General Purpose Registers
        self.reg = [0] * 8  # this is the CPU's register

        # Memory
        self.ram = [0] * 256 # size of the computer's memory

        # Operations
        self.ops = [0] * 256

        # Instructions
        self.ins = Instructions(self)

        for key in operation_codes:
            self.ops[operation_codes[key]] = getattr(self.ins, "handle_" + key, 0)

    def load(self, program=None):
        """Load a program into memory."""

        address = 0

        if program == None:
            # Default program
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while True:
            self.ir = self.ram_read(self.pc)

            arguments = []
            # Build arguments array
            for index in range((self.ir >> 6)):
                arguments.append(self.ram_read(self.pc+1+index))

            # Call the standard instruction and pass to arguments array
            if self.ops[self.ir]:
                self.ops[self.ir](*arguments)
            else:
                print(f"Unknown Operations Code: {self.ir} Program Counter: {self.pc}.")
                break

            # Increment the program counter
            if (self.ir & 0b00010000) == 0:
                self.pc = (self.pc + ((self.ir >> 6) + 1)) & 0b11111111

    def ram_read(self, address = None):
        if address is not None:
            self.mar = address

        self.mdr = self.ram[self.mar]
        return self.mdr

    def ram_write(self, address = None, value = None):
        if address is not None:
            self.mar = address
        if value is not None:
            self.mdr = value

        self.ram[self.mar] = self.mdr

 
if __name__ == "__main__":
    cpu = CPU()
    print(len(cpu.ram))

    cpu.ram_write()
    print(cpu.ram[3])
