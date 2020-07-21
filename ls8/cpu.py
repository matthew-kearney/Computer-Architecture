"""CPU functionality."""
LDI = 0b10000010 # Set value of a register to integer
PRN = 0b01000111 # Print numeric value
HLT = 0b00000001 # exit the emulator

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        # general reg
        self.reg = [0] * 8
        # holds 256 bytes
        self.ram = [0] * 256
        # program counter
        self.pc = 0 
        
    def ram_read(self, mar):
        # accept the address to read
        # MAR holds address that is being read or written
        mdr = self.ram[mar]
        # return stored value
        # MDR holds data that was read or wrote
        return mdr
    
    def ram_write(self, mar, value):
        # should accept a value to write and adress to write it
        self.ram[mar] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running: 
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1) 
            operand_b = self.ram_read(self.pc + 2)
            # sets a specified register to a specified value
            if opcode == LDI: 
                self.reg[operand_a] = operand_b
                # skip down 3 to PRN
                self.pc += 3 
                
            # prints the numeric value stored in a register
            elif opcode == PRN: 
                print(self.reg[operand_a])
                #skip down 2 to HLT
                self.pc += 2 

            elif opcode == HLT:
                running = False 

            else:
                print(f"Unknown instruction: {opcode}")
                sys.exit(1)
