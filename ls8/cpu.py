"""CPU functionality."""

import sys

program = []

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # creates ram with 256 bytes of memory
        self.pc = 0  # our counter
        self.reg = [0] * 8  # general registry with 8 slots
        # instruction code link with shorter name for development sake
        self.instructions = {"LDI": 0b10000010,
                            "HLT": 0b00000001,
                            "PRN": 0b01000111,
                            "MUL": 0b10100010,
                            }  # instruction code link with short name for development sake

    def ram_read(self, ma):
        # ma = Memory Access
        return self.ram[ma]

    def ram_write(self, ma, v):
        # v = value
        self.ram[ma] = v
        
        
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
        # if len(sys.argv) > 1:
        #     program_file = sys.argv[1]
        #     with open(program_file) as f:
        #         for line in f:
        #             line = line.split('#')
        #             line = line[0].strip()
        #             if line == '':
        #                 continue
        #             line = int(line, 2)
        #             program.append(line)
        # else:
        #     return

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
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == self.instructions["HLT"]:
                running = False
                self.pc += 1
            elif IR == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == self.instructions["PRN"]:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.instructions["MUL"]:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            else:
                print(f"Instruction unkown")
                running = False
