#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# Command Line Arguments (CLA)
cla = {}

if len(sys.argv) > 1:
    for index in range(1, len(sys.argv)):
        cla = sys.argv[index]

        #Split arguments into resources
        resource = cla.split('=', 1)
        #Ignore leading dashes
        if resource[0].startswith('-') or resource[0].startswith('--'):
            pass

        if len(resource) == 2:
            #Resource has value
            cla[resource[0]] = resource[1]
        elif len(resource) == 1:
            cla[resource[0]] = 1
        else:
            #Skip if invalid
            pass

print("Command Line Arguments:", cla)

file_name = cla.get('file', 'examples/mult.ls8')
base = cla.get('base', 2)

if file_name:
    try:
        memory = [0] * 256
        address = 0

        with open(file_name) as open_file:
            for line in open_file:
                line = line.strip()
                line = line.split('#', 1)[0]

                if address < len(memory):
                    try:
                        line = int(line, base)
                        memory[address] = line
                        address += 1
                    except ValueError:
                        pass
                else:
                    print("Memory overflow.  Load not completed.")
                    break

        cpu.load(memory)
    except FileNotFoundError:
        print(f"Unable to find {file_name}.")
        sys.exit(1)

else:
    cpu.load()

cpu.run()