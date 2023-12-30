# RISC-V Assembler
#
# This program assembles RISC-V instructions into a binary file
#
# ISA and other design choices based on these specific input files (not all RISC-V instructions are implemented)
#
# Inputs are assumed to be correct (error checking is lacking)
#
# Run: python3.11 main.py <source_code> <objFiles> <output>
#
# = Structure of the output file = 
#
# Immediates/memory addresses are big endian (only entry_point_addr is little endian)
#
#   |-----------------------|
#   |  variables/constants  |
#   |   declared in data    | <- starts at a bit address multiple of 8
#   |       section         |
#   |-----------------------|
#   | machine code computed |
#   |    from .s file       |
#   |-----------------------|
#   |   machine code from   |
#   |   linked obj files    |
#   |-----------------------|
#   |    entry_point_addr   | <- start of the binary output file
#   |          2B           | 
#   |-----------------------|

import sys
import re

# OPCODES dictionary ~ encoded using huffman coding (frequencies based on our 12 functions)
OPCODE = {"addi": [1, 1, 0], "add": [0, 0, 1], "j": [1, 1, 1, 1], "ret": [1, 0, 1, 1], 
          "li": [1, 0, 1, 0], "bge": [1, 0, 0, 0], "beqz": [1, 1, 1, 0, 1], "fmv.s": [1, 1, 1, 0, 0], 
          "sd": [1, 0, 0, 1, 1], "lb": [0, 1, 1, 1, 1], "call": [0, 1, 1, 0, 1], "sb": [0, 1, 1, 0, 0], 
          "lw": [0, 1, 0, 1, 1], "ld": [0, 1, 0, 1, 0], "flt.s": [0, 0, 0, 1, 1], "fld": [0, 0, 0, 1, 0], 
          "la": [1, 0, 0, 1, 0, 1], "fsw": [1, 0, 0, 1, 0, 0], "slli": [0, 1, 1, 1, 0, 1], "flw": [0, 1, 1, 1, 0, 0], 
          "srai": [0, 1, 0, 0, 0, 1], "fmul.d": [0, 0, 0, 0, 1, 1], "fsub.d": [0, 0, 0, 0, 1, 0], 
          "fsqrt.d": [0, 1, 0, 0, 1, 1, 1], "fadd.d": [0, 1, 0, 0, 1, 1, 0], "fmv.s.x": [0, 1, 0, 0, 1, 0, 1], 
          "bgt": [0, 1, 0, 0, 1, 0, 0], "bnez": [0, 1, 0, 0, 0, 0, 1], "sub": [0, 1, 0, 0, 0, 0, 0], 
          "fadd.s": [0, 0, 0, 0, 0, 1, 1], "fmul.s": [0, 0, 0, 0, 0, 1, 0], "mul": [0, 0, 0, 0, 0, 0]}

# Register codes dictionary ~ encoded using huffman coding (frequencies based on our 12 functions)
REG_DICT = {"t0": [1, 1, 1], 
            "t1": [0, 1, 1],     
            "a0": [0, 0, 1],     
            "sp": [1, 1, 0, 0],  
            "ft0": [1, 0, 1, 1], 
            "a1": [1, 0, 1, 0],  
            "t3": [1, 0, 0, 0],  
            "ft1": [0, 1, 0, 1], 
            "t2": [0, 1, 0, 0],  
            "zero": [0, 0, 0, 1],
            "t4": [1, 1, 0, 1, 1],
            "a2": [1, 1, 0, 1, 0],
            "t5": [1, 0, 0, 1, 1, 1],
            "s1": [1, 0, 0, 1, 1, 0],
            "fa0": [0, 0, 0, 0, 0],
            "fa2": [1, 0, 0, 1, 0, 0],
            "fa1": [0, 0, 0, 0, 1, 1],
            "ra": [0, 0, 0, 0, 1, 0],
            "ft2": [1, 0, 0, 1, 0, 1, 1, 1],
            "ft3": [1, 0, 0, 1, 0, 1, 0],
            "a3": [1, 0, 0, 1, 0, 1, 1, 0, 1],
            "ft11": [1, 0, 0, 1, 0, 1, 1, 0, 0, 1],
            "ft10": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1],
            "ft9": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1],
            "ft8": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
            "fs11": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            "fs10": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs9": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs8": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs7": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs6": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs5": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs4": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs3": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs2": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa7": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa6": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa5": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa4": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa3": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs1": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs0": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft7": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft6": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft5": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft4": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "t6": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s11": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s10": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s9": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s8": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s7": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s6": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s5": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],        
            "s4": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],     
            "s3": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  
            "s2": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a7": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a6": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a5": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a4": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s0": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "tp": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "gp": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
            # long encodings occour due to some registers not being used at all in our 12 functions

label_addresses = []    # list with labels and their addresses
curr_address = 0        # bit counter used in real instruction processing
simulated_address = 0   # bit counter used to simulate addresses in process_labels function
                        # also used as an offset for setting global variables addresses  (global variables 
                        # are written right after instructions)
MEM_ADDRESS_SIZE = 16   # enough for 8 kB = 65536 bits of memory (each bit has its own address)
IMMEDIATE_SIZE = 32     # instructions with immediates that can not be represented in 32 bits are expanded

bit_queue = []
def write_bits(bits_arr):
    bit_queue.extend(bits_arr)
    while len(bit_queue) >= 8 :
        byte = 0
        for i in range(8):
            byte = byte << 1
            byte = byte | bit_queue[0]
            del bit_queue[0]
        with open(bin_file_name, "ab") as binary_file:
            binary_file.write(bytearray([byte]))

# int_to_bit_arr returns the binary representation of an integer given as a string (2's complement)
# big endian
def int_to_bit_arr(string, size):
    num = int(string)

    if num >= 0:
        bin_val = bin(num)
        bin_arr = [0]*(size-len(bin_val)+2)
        bin_arr.extend([int(bin_val[i]) for i in range(2,len(bin_val))])
    else:
        bin_val = bin(abs(num)-1)
        bin_arr = bin_arr = [1]*(size-len(bin_val)+2)
        bin_arr.extend([~int(bin_val[i]) & 1 for i in range(2,len(bin_val))])
    if len(bin_arr) <= size:
        return bin_arr
    else:
        print("something went wrong")
        return None

# search_addr_by_label searches the address of a label in the specified direction (f/b)
# returns a 16 bit array with the memory address of the first occourance found
def search_addr_by_label(label, curr_addr):
    direction = label[-1]
    label = label[:-1]
    if direction == "f":
        for elem in label_addresses:
            if elem[0] == label and elem[1] > curr_addr:
                return addr_to_bits(elem[1])
    else:
        for i in range(len(label_addresses)-1,-1,-1):
            if label_addresses[i][0] == label and label_addresses[i][1] <= curr_addr:
                return addr_to_bits(label_addresses[i][1]) 

    print("something wrong happened")

# addr_to_bits transforms an integer (an address) into a 16 bit array (mem_addr_size)
# big endian   
def addr_to_bits(addr):
    if addr < 0:
        print("address must be positive")
        return None
    return [int(bit) for bit in bin(addr)[2:].zfill(MEM_ADDRESS_SIZE)]

# process_labels creates a list with addresses of labels used in the code by passing once through all instructions
# this list is sorted by default in ascending order
def process_labels(file_name):
    global simulated_address
    f = open(file_name)
    for line in f:
        line = line.lstrip().rstrip()

        if line == "":
            continue        # ignore blank lines
        if line[0] == "#":
            continue        # ignore comments
        
        # remove comments from instructions
        line = line.split("#")[0].rstrip()
        
        # set section (only read only data section is implemented)
        if line == ".section .rodata":
            current_section = 1
            continue
        elif line == ".section .text":
            current_section = 2
            continue
        elif ".global" in line:
            # skip line (execution starts at address 0 no matter what)
            continue

        if current_section == 1:        # data section ~ save global variables
            # skip data section
            continue

        if (line[-1] == ":"):           # save label address
            label_addresses.append((line[:-1], simulated_address))
            continue

        # SIMULATE INSTRUCTIONS

        line = re.split("[ ,]+",line)
        line[0]=line[0].lower()
        if line[0] == "addi":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + IMMEDIATE_SIZE

        elif line[0] == "slli" or line[0] == "srai":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + 6

        elif line[0] == "j":
            simulated_address += len(OPCODE[line[0]]) + MEM_ADDRESS_SIZE
        
        elif line[0] == "mul":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

        elif line[0] == "li":
            immediate_val = int(line[2])
            if -2147483648 <= immediate_val <= 2147483647:
                simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE
            else:
                lower_32_bits = immediate_val & 0xFFFFFFFF
                simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE
                simulated_address += len(OPCODE["slli"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + 6
                simulated_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE

                if lower_32_bits != 4294967295:
                    simulated_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE
                else:
                    simulated_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE
                    simulated_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE

        elif line[0] == "ret":
            simulated_address += len(OPCODE[line[0]])

        elif line[0] == "add":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])
        elif line[0] == "mv":
            simulated_address += len(OPCODE["add"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT["zero"])

        elif line[0] == "bge" or line[0] == "ble":
            simulated_address += len(OPCODE["bge"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + MEM_ADDRESS_SIZE

        elif line[0] == "beqz" or line[0] == "la" or line[0] == "bnez":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE

        elif (line[0] == "sd" or line[0] == "lb" or line[0] == "ld" or line[0] == "sb" or line[0] == "lw" or line[0] == "fld"
              or line[0] == "fsw" or line[0] == "flw"):
            reg = re.split("[()]+",line[2])
            reg = reg[1]
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

        elif line[0] == "call":
            simulated_address += len(OPCODE[line[0]]) + MEM_ADDRESS_SIZE

        elif (line[0] == "fsub.d" or line[0] == "fmul.d" or line[0] == "sub" 
              or line[0] == "fmul.s" or line[0] == "fadd.s" or line[0] == "fadd.d"):
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

        elif line[0] == "flt.s" or line[0] == "fgt.s":
            simulated_address += len(OPCODE["flt.s"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

        elif line[0] == "fsqrt.d" or line[0] == "fmv.s.x" or line[0] == "fmv.s":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]])

        elif line[0] == "bgt":
            simulated_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + MEM_ADDRESS_SIZE
    
    # allignment for global variables
    simulated_address += 8 - simulated_address%8

    f.close()

# I/O Files
code_file_name = sys.argv[1]
linked_obj_files = sys.argv[2:-1]
bin_file_name = sys.argv[-1]

# clears output file before writing
open(bin_file_name,"w").close()

# Link machine code from other obj files
# expected format: label table, text section   (extern variables are not implemented here) 
# label table is sorted and ends with a special row 
# for our example, cfunc.h will be transformed as follows (in binary of course):
# label table: [["cfunc",16_bit_mem_addr],[0]]; text section: mul a1,a1,a2; add a0,a0,a1; ret

if linked_obj_files != []:
    for file in linked_obj_files:
        # fetch label table
        file = open(file, "rb")
        bit_pointer = 0
        fetched_labels = []
        label_curr_str = []
        label_mem_addr = 0
        while byte := file.read(1):
            bit_pointer += 8
            if label_curr_str == [] and label_mem_addr == 0 and byte == b'\x00':
                # if we encounter [0], the whole table has been fetched
                break
            if byte != b'\x00':
                # read ascii char
                label_curr_str.append(chr(int.from_bytes(byte)))
            else:
                # if we reach the end of the label name, fetch 2 bytes 
                # (the memory address the label points to in the original obj file) and store them
                byte = file.read(2)
                bit_pointer += 8*2
                label_mem_addr = int.from_bytes(byte)
                fetched_labels.append((''.join(label_curr_str),label_mem_addr))
                label_curr_str = []
                label_mem_addr = 0

        # copy the rest of the binary
        while byte := file.read(1):
            if fetched_labels != [] and bit_pointer == fetched_labels[0][1]:
                label_addresses.append((fetched_labels[0][0],curr_address))
                del fetched_labels[0]
            with open(bin_file_name, "ab") as binary_file:
                binary_file.write(byte)
            curr_address += 8
            simulated_address += 8
            bit_pointer += 8
        
        file.close()

# process labels
process_labels(code_file_name)

f = open(code_file_name)

# Start outputing machine code from instructions

current_section = 0         # data/text sections
glb_var = {}                # dictionary with global variable addresses
glb_var_bits = []           # retains global variables in binary so they can be added after the text section
temp_var_addr = 0           # used to calculate global variable addresses
entry_label = ""            # saves the entry label
for line in f:
    line = line.lstrip().rstrip()

    if line == "":
        continue        # ignore blank lines
    if line[0] == "#":
        continue        # ignore comments
    
    # remove comments from instructions
    line = line.split("#")[0].rstrip()
    
    # set section (only read only data section is implemented)
    if line == ".section .rodata":
        current_section = 1
        continue
    elif line == ".section .text":
        current_section = 2
        continue
    elif ".global" in line:
        entry_label = line.split()[1]
        continue

    if current_section == 1:        # data section ~ save global constants
        # Note: only works with .rodata at the start of the code (may work in other cases too ??)
        # The following format is expected: <var_name>: <var_type> <value> (exactly one space to separate)
        var_name = line[:line.find(":")]
        var_type = line[line.find("."):].split()[0]
        var_arg = line[line.find(var_type)+len(var_type)+1:]
        
        glb_var[var_name] = temp_var_addr + simulated_address

        if var_type == ".asciz":
            for i in range(1,len(var_arg)-1):
                symbol_code = ord(var_arg[i])

                if symbol_code == 92:
                    # special character (only \n is implemented below)
                    continue
                if ord(var_arg[i-1]) == 92 and var_arg[i] == "n":
                    symbol_code = 10        # newline

                binary_ascii = list(map(int,list(bin(symbol_code)[2:])))
                binary_ascii[0:0] = [0]*(8-len(binary_ascii))
                glb_var_bits.extend(binary_ascii)
                temp_var_addr += 8
            
            glb_var_bits.extend([0,0,0,0,0,0,0,0])      # null asciz terminator
            temp_var_addr += 8
            
        # other data types are not implemented
        continue

    if (line[-1] == ":"):
        # ignore labels (processed separately)
        continue

    # START PROCESSING INSTRUCTIONS

    line = re.split("[ ,]+",line)
    line[0]=line[0].lower()
    if line[0] == "addi":
        # addi: reg1 = reg2 + 32-bits immediate (sign extended to 64 bits)
        # the add instruction can be used for values larger than 32 bits (or a combination of addi instructions)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(int_to_bit_arr(line[3], IMMEDIATE_SIZE))
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + IMMEDIATE_SIZE

    elif line[0] == "j":
        # jump to label
        write_bits(OPCODE[line[0]])
        address = search_addr_by_label(line[1], curr_address)
        write_bits(address)
        curr_address += len(OPCODE[line[0]]) + MEM_ADDRESS_SIZE

    elif line[0] == "li":
        # load immediate into reg
        immediate_val = int(line[2])
        if -2147483648 <= immediate_val <= 2147483647:
            # can be represented in 32 bits
            write_bits(OPCODE[line[0]])
            write_bits(REG_DICT[line[1]])
            write_bits(int_to_bit_arr(line[2], IMMEDIATE_SIZE))
            curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE
        else:
            # values from our 12 functions never reach this else branch  
            # immediate_val can not be represented in 32 bits, the instruction will be expanded
            upper_32_bits = (immediate_val & 0xFFFFFFFF00000000) >> 32
            lower_32_bits = immediate_val & 0xFFFFFFFF

            # load upper 32 bits
            # we do not care if the value is sign extended since we are going to shift it to the left
            write_bits(OPCODE["li"])
            write_bits(REG_DICT[line[1]])
            write_bits(int_to_bit_arr(str(upper_32_bits), IMMEDIATE_SIZE))
            curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE

            # shift the value to its place (32 bits to the left)
            write_bits(OPCODE["slli"])
            write_bits(REG_DICT[line[1]])
            write_bits(REG_DICT[line[1]])
            value = int_to_bit_arr("32", 6)
            write_bits(value)
            curr_address += len(OPCODE["slli"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + 6

            # add the lower 32 bits in multiple steps to avoid sign extension from the addi instruction
            # we try adding x/2 + x/2 + x%2 (= x) to avoid that
            # otherwise, if MSB is not zero, the sign extended value will change the upper bits
            # (strange and inefficient design but it makes use of already existing instructions from our 12 functions)
            write_bits(OPCODE["addi"])
            write_bits(REG_DICT[line[1]])
            write_bits(REG_DICT[line[1]])
            write_bits(int_to_bit_arr(str(lower_32_bits//2), IMMEDIATE_SIZE))
            curr_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE

            if lower_32_bits != 4294967295:
                # we can add lower_32_bits//2 + lower_32_bits%2 in one addi instruction
                write_bits(OPCODE["addi"])
                write_bits(REG_DICT[line[1]])
                write_bits(REG_DICT[line[1]])
                write_bits(int_to_bit_arr(str(lower_32_bits//2 + lower_32_bits%2), IMMEDIATE_SIZE))
                curr_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE
            else:
                # the value 2147483647 has the first 31 bits set, so we can not add the modulus in the same addi instruction
                # 2147483647 + 1 = 2^31 (32nd bit would be set)
                # we add the modulus in a separate addi instruction
                write_bits(OPCODE["addi"])
                write_bits(REG_DICT[line[1]])
                write_bits(REG_DICT[line[1]])
                write_bits(int_to_bit_arr("2147483647", IMMEDIATE_SIZE))    # 4294967295/2 = 2147483647.5
                curr_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE

                write_bits(OPCODE["addi"])
                write_bits(REG_DICT[line[1]])
                write_bits(REG_DICT[line[1]])
                write_bits(int_to_bit_arr("1", IMMEDIATE_SIZE))
                curr_address += len(OPCODE["addi"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[1]]) + IMMEDIATE_SIZE

    elif line[0] == "ret":
        # ret jumps to the address in ra register
        write_bits(OPCODE[line[0]])
        curr_address += len(OPCODE[line[0]])

    elif line[0] == "add":
        # reg1 = reg2 + reg3
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])
    elif line[0] == "mv":
        # mv: move reg2 in reg1 (<=> addi reg1, reg2, zero)
        write_bits(OPCODE["add"])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT["zero"])
        curr_address += len(OPCODE["add"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT["zero"])

    elif line[0] == "mul":
        # reg1 = reg2 * reg3
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "bge":
        # branch if reg1 is greater than or equal to reg2
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + MEM_ADDRESS_SIZE
    elif line[0] == "ble":
        # ble reg1,reg2,label (<=> bge reg2,reg1,label)
        write_bits(OPCODE["bge"])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[1]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(OPCODE["bge"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + MEM_ADDRESS_SIZE

    elif line[0] == "beqz":
        # branch if reg is equal to zero (could have been merged with beq but it is not implemented here)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        address = search_addr_by_label(line[2], curr_address)
        write_bits(address)
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE

    elif line[0] == "sd":
        # store 64 bits from reg to mem
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "fmv.s":
        # copy fp reg2 in reg1 (could be merged with another instruction but it is not implemented here)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]])

    elif line[0] == "lb":
        # load 8 bits from mem address, sign extend the value and store to reg
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "sb":
        # store 8 bits from reg to mem
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "call":
        # usual call behavior (which is hardcoded in the interpreter)
        # calls to mem addresses 65533, 65534, 65535 are reserved for strlen, scanf and printf
        # these mem addresses are still usable for read/write operations, just not for calls
        write_bits(OPCODE[line[0]])
        call_addr = -1
        if line[1] == "printf":
            call_addr = 65535
        elif line[1] == "scanf":
            call_addr = 65534
        elif line[1] == "strlen":
            call_addr = 65533
        for elem in label_addresses:
            if line[1] == elem[0]:
                call_addr = elem[1]
                break
        write_bits(addr_to_bits(call_addr))
        curr_address += len(OPCODE[line[0]]) + MEM_ADDRESS_SIZE

    elif line[0] == "ld":
        # load 64 bits from mem address and store to reg
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "lw":
        # load 32 bits from mem address, sign extend the value and store to reg
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "fld":
        # load 64 bits from mem address and store to reg (fp)
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "slli":
        # logical left shift on reg2 by amount held in immediate and store to reg1
        # immediate is an unsigned 6 bit value
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        value = int_to_bit_arr(line[3], 6)  # 6 bits are enough to encode 64 values
        print(value)
        write_bits(value)
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + 6

    elif line[0] == "fsw":
        # store 32 bit fp to memory address
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "la":
        # load address in register
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(addr_to_bits(glb_var[line[2]])) 
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE

    elif line[0] == "srai":
        # arithmetic right shift on reg2 by amount held in immediate and store to reg1
        # immediate is an unsigned 6 bit value
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        value = int_to_bit_arr(line[3], 6)  # 6 bits are enough to encode 64 values
        write_bits(value)
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + 6

    elif line[0] == "fsub.d":
        # reg1 = reg2 - reg3  ~  fp
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "fmul.d":
        # reg1 = reg2 * reg3  ~  fp
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "flt.s":
        # reg1 = reg2 < reg3    (boolean result)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])
    elif line[0] == "fgt.s":
        # reg1 = reg3 < reg2       (<=> flt.s reg1,reg3,reg2)
        write_bits(OPCODE["flt.s"])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[3]])
        write_bits(REG_DICT[line[2]])
        curr_address += len(OPCODE["flt.s"]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "flw":
        # load 32 bits fp from mem address and store to reg
        # offset has to fit in 16 bits (2's complement)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        offset = int_to_bit_arr(line[2].split("(")[0], MEM_ADDRESS_SIZE)
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(REG_DICT[reg])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE + len(REG_DICT[reg])

    elif line[0] == "sub":
        # reg1 = reg2 - reg3
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "bnez":
        # branch if reg is not equal to zero (could have been merged with bne but it is not implemented here)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        address = search_addr_by_label(line[2], curr_address)
        write_bits(address)
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + MEM_ADDRESS_SIZE

    elif line[0] == "fadd.d":
        # reg1 = reg2 + reg3  ~  fp
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "fsqrt.d":
        # reg1 = sqrt(reg2)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]])

    elif line[0] == "bgt":
        # branch if reg1 is greater than reg2
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + MEM_ADDRESS_SIZE

    elif line[0] == "fmv.s.x":
        # reg1 = reg2 (move from integer register to fp register)
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]])

    elif line[0] == "fmul.s":
        # reg1 = reg2 * reg3  ~  fp
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

    elif line[0] == "fadd.s":
        # reg1 = reg2 + reg3  ~  fp
        write_bits(OPCODE[line[0]])
        write_bits(REG_DICT[line[1]])
        write_bits(REG_DICT[line[2]])
        write_bits(REG_DICT[line[3]])
        curr_address += len(OPCODE[line[0]]) + len(REG_DICT[line[1]]) + len(REG_DICT[line[2]]) + len(REG_DICT[line[3]])

# allignment for global variables
curr_address += 8 - len(bit_queue)
write_bits([0] * (8 - len(bit_queue)))

# write global variables in object file
curr_address += len(glb_var_bits)
write_bits(glb_var_bits)

# Insert entry point address at the start of the file (should be fine with small file sizes)
with open(bin_file_name,"rb") as original:
    existing_content = original.read()
with open(bin_file_name,"wb") as output:
    for elem in label_addresses:
        if entry_label == elem[0]:
            output.write(elem[1].to_bytes(2, byteorder = "little"))
            break
with open(bin_file_name,"ab") as output:
    output.write(existing_content)

write_bits([0]*7)   # flush bits that are still in the queue

f.close()
