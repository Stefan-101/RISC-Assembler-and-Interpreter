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

# immediate_to_bits returns the binary representation of an integer given as a string (2's complement)
# What size are the registers ??? !!!
immediate_size = 32
def immediate_to_bits(string):
    num = int(string)

    if num >= 0:
        bin_val = bin(num)
        bin_arr = [0]*(32-len(bin_val)+2)
        bin_arr.extend([int(bin_val[i]) for i in range(2,len(bin_val))])
    else:
        bin_val = bin(abs(num)-1)
        bin_arr = bin_arr = [1]*(32-len(bin_val)+2)
        bin_arr.extend([~int(bin_val[i]) & 1 for i in range(2,len(bin_val))])
    return bin_arr

mem_address_size = 17
def search_addr_by_label(label, curr_addr):
    # TODO implementation (after process_labels is implemented)
    # return dummy value for now    
    return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

def process_labels(file_name):
    f = open(file_name)
    for line in f:
        # TODO proccess label addresses by simulating instructions
        pass
    f.close()

# I/O Files
bin_file_name = "temp.o"
code_file_name = "instr_tester.txt"
f = open(code_file_name)

# TEMP
temp = open(bin_file_name,"w")
temp.close()

# OPCODES dictionary ~ encoded using huffman coding (frequencies based on our 12 functions)
opcode = {"addi":[1, 1, 1], "j":[1, 1, 0, 1], "ret":[1, 1, 0, 0], "li":[1, 0, 1, 1], 
          "add":[1, 0, 0, 0], "bge":[0, 1, 0, 0], "beqz":[0, 0, 0, 0], "mv":[1, 0, 1, 0, 1], 
          "fmv.s":[1, 0, 0, 1, 1], "sd":[1, 0, 0, 1, 0], "lb":[0, 1, 1, 1, 1], "call":[0, 1, 1, 0, 1], 
          "sb":[0, 1, 1, 0, 0], "lw":[0, 1, 0, 1, 1], "ld":[0, 1, 0, 1, 0], "fld":[0, 0, 0, 1, 1], 
          "la":[1, 0, 1, 0, 0, 1], "fsw":[1, 0, 1, 0, 0, 0], "slli":[0, 1, 1, 1, 0, 1], 
          "flw":[0, 1, 1, 1, 0, 0], "fmul.d":[0, 0, 1, 1, 1, 1], "fsub.d":[0, 0, 1, 1, 1, 0], 
          "flt.s":[0, 0, 1, 1, 0, 1], "fgt.s":[0, 0, 1, 1, 0, 0], "ble":[0, 0, 1, 0, 0, 1], 
          "srai":[0, 0, 1, 0, 0, 0], "bnez":[0, 0, 1, 0, 1, 1, 1], "sub":[0, 0, 1, 0, 1, 1, 0], 
          "fsqrt.d":[0, 0, 1, 0, 1, 0, 1], "fadd.d":[0, 0, 1, 0, 1, 0, 0], "fmv.s.x":[0, 0, 0, 1, 0, 1, 1], 
          "bgt":[0, 0, 0, 1, 0, 1, 0], "fadd.s":[0, 0, 0, 1, 0, 0, 1], "fmul.s":[0, 0, 0, 1, 0, 0, 0]}
# TODO Instructions to be merged (recalculate huffman encodings)
# mv -> addi
# ble -> bge    



# Register codes dictionary ~ encoded using huffman coding (frequencies based on our 12 functions)
reg_dict = {"t0": [1, 1, 1], 
            "t1": [1, 0, 0],     
            "a0": [0, 0, 1],     
            "sp": [1, 1, 0, 1],  
            "ft0": [1, 0, 1, 1], 
            "a1": [1, 0, 1, 0],  
            "t3": [0, 1, 1, 1],  
            "ft1": [0, 1, 0, 1], 
            "t2": [0, 1, 0, 0],
            "t4": [0, 0, 0, 1],
            "a2": [1, 1, 0, 0, 1],
            "zero": [0, 0, 0, 0, 1],
            "t5": [1, 1, 0, 0, 0, 1],
            "s1": [1, 1, 0, 0, 0, 0],
            "fa0": [0, 0, 0, 0, 0],
            "fa2": [0, 1, 1, 0, 1, 0],
            "fa1": [0, 1, 1, 0, 0, 1],
            "ra": [0, 1, 1, 0, 0, 0],
            "ft2": [0, 1, 1, 0, 1, 1, 1, 1],
            "ft3": [0, 1, 1, 0, 1, 1, 0],
            "a3": [0, 1, 1, 0, 1, 1, 1, 0, 1],
            "ft11": [0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
            "ft10": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            "ft9": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            "ft8": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            "fs11": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            "fs10": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs9": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs8": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs7": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs6": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs5": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs4": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs3": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs2": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa7": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa6": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa5": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa4": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fa3": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs1": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "fs0": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft7": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft6": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft5": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "ft4": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "t6": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s11": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s10": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s9": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s8": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s7": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s6": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s5": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],        
            "s4": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],     
            "s3": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  
            "s2": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a7": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a6": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a5": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "a4": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "s0": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "tp": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "gp": [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
            # long encodings occour due to some registers not being used at all in our 12 functions

current_section = 0
curr_address = 0
glb_var={}
for line in f:
    line = line.lstrip().rstrip()

    if line == "":
        continue        # ignore blank lines
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


    if current_section == 1:        # data section
        # Note: only works with .rodata at the start of the code
        var_name = line[:line.find(":")]
        var_type = line[line.find("."):].split()[0]
        var_arg = line[line.find(var_type)+len(var_type)+1:]
        
        glb_var[var_name] = curr_address

        if var_type == ".asciz":
            bytes_written = 1           # consider null terminator written
            for i in range(1,len(var_arg)-1):
                symbol_code = ord(var_arg[i])

                if symbol_code == 92:
                    # special character (only \n is implemented below)
                    continue
                if ord(var_arg[i-1]) == 92:
                    if var_arg[i] == "n":
                        symbol_code = 10        # newline

                binary_ascii = list(map(int,list(bin(symbol_code)[2:])))
                binary_ascii[0:0] = [0]*(8-len(binary_ascii))
                write_bits(binary_ascii)
                bytes_written += 1
            
            write_bits([0,0,0,0,0,0,0,0])     # null asciz terminator
            
            curr_address += 8*bytes_written

        # implementation for other data types ..
        continue

    if (line[-1] == ":"):
        # ignore labels (processed separately)
        continue

    # start processing instructions

    line = re.split("[ ,]+",line)
    # TODO line[0] to lowercase ??
    if line[0].lower() == "addi":
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(immediate_to_bits(line[3]))
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_size

    elif line[0].lower() == "j":
        # jump to label
        write_bits(opcode[line[0]])
        address = search_addr_by_label(line[1], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + mem_address_size

    elif line[0].lower() == "li":
        # load immediate into reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(immediate_to_bits(line[2]))
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size

    elif line[0].lower() == "ret":
        # ret will end the execution for our functions
        write_bits(opcode[line[0]])
        curr_address += len(opcode[line[0]])

    elif line[0].lower() == "add":
        # reg1 = reg2 + reg3
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0].lower() == "bge":
        # branch if reg1 is greater than or equal to reg2
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + mem_address_size

    elif line[0].lower() == "beqz":
        # branch if reg is equal to zero (could have been merged with beq but it is not implemented here)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        address = search_addr_by_label(line[2], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + mem_address_size

    elif line[0].lower() == "mv":
        # move reg2 to reg1
        # TODO can be merged with addi ? (mv reg1, reg2 <=> add reg1,reg2,zero)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]])

    elif line[0].lower() == "sd":
        # store 64 bits (????) from reg to mem  !!!
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "fmv.s":
        # copy fp reg2 in reg1 (could be merged with another instruction but it is not implemented here)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]])

    elif line[0].lower() == "lb":
        # load 8 bits from mem address, sign extend the value and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "sb":
        # store 8 bits from reg to mem
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "call":
        # could be expanded, but instructions from expansion are not implemented (will be hardcoded in the interpreter)
        write_bits(opcode[line[0]])
        func_name = line[1]
        write_bits([1,1,1,1,1,1,1,1])   # DUMMY value
        func_name_length = 8
        curr_address += len(opcode[line[0]]) + func_name_length
        # TODO encode function name

    elif line[0].lower() == "ld":
        # load 64 bits (???) from mem address and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "lw":
        # load 32 bits from mem address, sign extend the value (???) and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "fld":
        # load 64 bits (???) from mem address and store to reg (fp)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "slli":
        # logical left shift on reg2 by amount held in immediate and store to reg1
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        value = immediate_to_bits(line[3])
        write_bits(value)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_size

    elif line[0].lower() == "fsw":
        # store 32 bit fp to memory address
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0].lower() == "la":
        # load address in register
        # TODO can be merged with LI instruction ? (LA reg1, var_name <=> LI reg1, $var_name)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(immediate_to_bits(glb_var[line[2]]))
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size

    elif line[0].lower() == "srai":
        # arithmetic right shift on reg2 by amount held in immediate and store to reg1
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        value = immediate_to_bits(line[3])
        write_bits(value)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_size

    elif line[0].lower() == "ble":
        # TODO can be merged with BGE instruction ? (ble reg1,reg2,label <=> bge reg2,reg1,label)
        # branch if reg1 is less than or equal to reg2
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + mem_address_size

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
