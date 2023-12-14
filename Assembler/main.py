import re

bit_stack = []
def write_bits(bits_arr):
    global bit_stack
    bit_stack.extend(bits_arr)
    while len(bit_stack) >=8 :
        byte = 0
        for i in range(8):
            byte = byte << 1
            byte = byte | bit_stack[0]
            del bit_stack[0]
        with open(bin_file_name, "ab") as binary_file:
            binary_file.write(bytearray([byte]))

def process_labels(file_name):
    f = open("file_name")
    for line in f:
        # TODO proccess label addresses by simulating instructions
        pass
    f.close()

# I/O Files
bin_file_name = "func_1.o"
code_file_name = "func_1.txt"
f = open(code_file_name)

# OPCODES dictionary
# TODO opcode dictionary
opcode = {"addi": [1,1,1], "j": [1101]}

# Register codes dictionary
# TODO register dictionary
reg_dict = {}

current_section = 0
curr_address = 0
labels = []
for line in f:
    line = line.lstrip().rstrip()

    if line[0] == "#":
        continue        # ignore comments
    
    # remove comments from instructions
    line = line.split("#")[0].rstrip()
    
    # set section
    if line == ".section .rodata":
        current_section = 1
        continue
    elif line == ".section .text":
        current_section = 2
        continue
    elif ".global" in line:
        # set entry label
        entry_label = line.split()[1]
        continue


    if current_section == 1:
        # TODO save global variables
        pass
        #continue       ~ go to next line TODO uncomment after implementation

    if (line[-1] == ":"):
        # save label address
        labels.append((line[:len(line)-1],curr_address))
        continue

    # start processing instructions

    line = re.split("[ ,]+",line)
    if line[0].lower() == "addi":
        # TODO implementation
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits([0,0,0,0,0,0,0,1])   # TODO transform immediate value to byte array
        immediate_length = 8    # TEMPORARY ~ need immediat value byte transformation
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_length
    elif line[0].lower() == "j":
        # TODO implementation
        pass
    elif line[0].lower() == "li":
        # TODO implementation
        pass
    elif line[0].lower() == "ret":
        # TODO implementation
        pass
    elif line[0].lower() == "add":
        # TODO implementation
        pass
    elif line[0].lower() == "bge":
        # TODO implementation
        pass
    elif line[0].lower() == "beqz":
        # TODO implementation
        pass
    elif line[0].lower() == "mv":
        # TODO implementation
        pass
    elif line[0].lower() == "sd":
        # TODO implementation
        pass
    elif line[0].lower() == "fmv.s":
        # TODO implementation
        pass
    elif line[0].lower() == "lb":
        # TODO implementation
        pass
    elif line[0].lower() == "sb":
        # TODO implementation
        pass
    elif line[0].lower() == "call":
        # TODO implementation
        pass
    elif line[0].lower() == "ld":
        # TODO implementation
        pass
    elif line[0].lower() == "lw":
        # TODO implementation
        pass
    elif line[0].lower() == "fld":
        # TODO implementation
        pass
    elif line[0].lower() == "slli":
        # TODO implementation
        pass
    elif line[0].lower() == "fsw":
        # TODO implementation
        pass
    elif line[0].lower() == "la":
        # TODO implementation
        pass
    elif line[0].lower() == "srai":
        # TODO implementation
        pass
    elif line[0].lower() == "ble":
        # TODO implementation
        pass
    elif line[0].lower() == "fsub.d":
        # TODO implementation
        pass
    elif line[0].lower() == "fmul.d":
        # TODO implementation
        pass
    elif line[0].lower() == "fgt.s":
        # TODO implementation
        pass
    elif line[0].lower() == "flt.s":
        # TODO implementation
        pass
    elif line[0].lower() == "flw":
        # TODO implementation
        pass
    elif line[0].lower() == "sub":
        # TODO implementation
        pass
    elif line[0].lower() == "bnez":
        # TODO implementation
        pass
    elif line[0].lower() == "fadd.d":
        # TODO implementation
        pass
    elif line[0].lower() == "fsqrt.d":
        # TODO implementation
        pass
    elif line[0].lower() == "bgt":
        # TODO implementation
        pass
    elif line[0].lower() == "fmv.s.x":
        # TODO implementation
        pass
    elif line[0].lower() == "fmul.s":
        # TODO implementation
        pass
    elif line[0].lower() == "fadd.s":
        # TODO implementation
        pass

write_bits([0,0,0,0,0,0,0,0])   # write unwritten bits still in the stack
