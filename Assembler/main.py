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
# NOTE What size are the registers ??? !!!
immediate_size = 7              # our maximum value is 32 -> we only need 7 bits to represent that in 2's complement
def immediate_to_bits(string):
    num = int(string)

    if num >= 0:
        bin_val = bin(num)
        bin_arr = [0]*(immediate_size-len(bin_val)+2)
        bin_arr.extend([int(bin_val[i]) for i in range(2,len(bin_val))])
    else:
        bin_val = bin(abs(num)-1)
        bin_arr = bin_arr = [1]*(immediate_size-len(bin_val)+2)
        bin_arr.extend([~int(bin_val[i]) & 1 for i in range(2,len(bin_val))])
    return bin_arr

mem_address_size = 16
def search_addr_by_label(label, curr_addr):
    # TODO implementation (after process_labels is implemented)
    # return dummy value for now    
    return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

#   addr_to_bits transforms an integer (an address) into a 16 bit array (mem_addr_size)
def addr_to_bits(addr):
    bin_val = bin(addr)
    bin_arr = [0]*(mem_address_size-len(bin_val)+2)
    bin_arr.extend([int(bin_val[i]) for i in range(2,len(bin_val))])
    return bin_arr

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
opcode = {"addi": [1, 1, 0], "add": [0, 1, 0], "j": [1, 1, 1, 1], 
          "ret": [1, 0, 1, 1], "li": [1, 0, 1, 0], "bge": [1, 0, 0, 0], 
          "beqz": [0, 0, 0, 0], "fmv.s": [1, 1, 1, 0, 0], "sd": [1, 0, 0, 1, 1], 
          "call": [0, 1, 1, 1, 1], "sb": [0, 1, 1, 1, 0], "lw": [0, 1, 1, 0, 1], 
          "ld": [0, 1, 1, 0, 0], "lb": [0, 0, 1, 1, 1], "flt.s": [0, 0, 1, 1, 0], 
          "fld": [0, 0, 0, 1, 1], "la": [1, 1, 1, 0, 1, 0], "fsw": [1, 0, 0, 1, 0, 1], 
          "slli": [1, 0, 0, 1, 0, 0], "flw": [1, 1, 1, 0, 1, 1, 1], "fmul.d": [1, 1, 1, 0, 1, 1, 0], 
          "fsub.d": [0, 0, 1, 0, 0, 1], "srai": [0, 0, 1, 0, 0, 0], "bnez": [0, 0, 1, 0, 1, 1, 1], 
          "sub": [0, 0, 1, 0, 1, 1, 0], "fsqrt.d": [0, 0, 1, 0, 1, 0, 1], "fadd.d": [0, 0, 1, 0, 1, 0, 0], 
          "fmv.s.x": [0, 0, 0, 1, 0, 1, 1], "bgt": [0, 0, 0, 1, 0, 1, 0], "fadd.s": [0, 0, 0, 1, 0, 0, 1], 
          "fmul.s": [0, 0, 0, 1, 0, 0, 0]}

# Register codes dictionary ~ encoded using huffman coding (frequencies based on our 12 functions)
reg_dict = {"t0": [1, 1, 1], 
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

    # START PROCESSING INSTRUCTIONS

    line = re.split("[ ,]+",line)
    line[0]=line[0].lower()
    if line[0] == "addi":
        # addi: reg1 = reg2 + immediate (sign extended)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(immediate_to_bits(line[3]))
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_size

    elif line[0] == "j":
        # jump to label
        write_bits(opcode[line[0]])
        address = search_addr_by_label(line[1], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + mem_address_size

    elif line[0] == "li":
        # load immediate into reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(immediate_to_bits(line[2]))
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size

    elif line[0] == "ret":
        # ret will end the execution for our functions
        write_bits(opcode[line[0]])
        curr_address += len(opcode[line[0]])

    elif line[0] == "add":
        # reg1 = reg2 + reg3
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])
    elif line[0] == "mv":
        # mv: move reg2 in reg1 (<=> addi reg1, reg2, zero)
        write_bits(opcode["add"])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict["zero"])
        curr_address += len(opcode["add"]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict["zero"])

    elif line[0] == "bge":
        # branch if reg1 is greater than or equal to reg2
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + mem_address_size
    elif line[0] == "ble":
        # ble reg1,reg2,label (<=> bge reg2,reg1,label)
        write_bits(opcode["bge"])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[1]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(opcode["bge"]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + mem_address_size

    elif line[0] == "beqz":
        # branch if reg is equal to zero (could have been merged with beq but it is not implemented here)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        address = search_addr_by_label(line[2], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + mem_address_size

    elif line[0] == "sd":
        # store 64 bits (????) from reg to mem  !!!
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "fmv.s":
        # copy fp reg2 in reg1 (could be merged with another instruction but it is not implemented here)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]])

    elif line[0] == "lb":
        # load 8 bits from mem address, sign extend the value and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "sb":
        # store 8 bits from reg to mem
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "call":
        # could be expanded, but instructions from expansion are not implemented (will be hardcoded in the interpreter)
        write_bits(opcode[line[0]])
        func_name = line[1]
        write_bits([1,1,1,1,1,1,1,1])   # DUMMY value
        func_name_length = 8
        curr_address += len(opcode[line[0]]) + func_name_length
        # TODO encode function name

    elif line[0] == "ld":
        # load 64 bits (???) from mem address and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "lw":
        # load 32 bits from mem address, sign extend the value (???) and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "fld":
        # load 64 bits (???) from mem address and store to reg (fp)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "slli":
        # logical left shift on reg2 by amount held in immediate and store to reg1
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        value = immediate_to_bits(line[3])
        write_bits(value)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_size

    elif line[0] == "fsw":
        # store 32 bit fp to memory address
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "la":
        # load address in register
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(addr_to_bits(glb_var[line[2]])) 
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + mem_address_size

    elif line[0] == "srai":
        # arithmetic right shift on reg2 by amount held in immediate and store to reg1
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        value = immediate_to_bits(line[3])
        write_bits(value)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + immediate_size

    elif line[0] == "fsub.d":
        # reg1 = reg2 - reg3  ~  fp
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0] == "fmul.d":
        # reg1 = reg2 * reg3  ~  fp
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0] == "flt.s":
        # reg1 = reg2 < reg3    (boolean result)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])
    elif line[0] == "fgt.s":
        # reg1 = reg3 < reg2       (<=> flt.s reg1,reg3,reg2)
        write_bits(opcode["flt.s"])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[3]])
        write_bits(reg_dict[line[2]])
        curr_address += len(opcode["flt.s"]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0] == "flw":
        # load 32 bits fp from mem address and store to reg
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        offset = immediate_to_bits(line[2].split("(")[0])
        write_bits(offset)
        reg = re.split("[()]+",line[2])
        reg = reg[1]
        write_bits(reg_dict[reg])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + immediate_size + len(reg_dict[reg])

    elif line[0] == "sub":
        # reg1 = reg2 - reg3
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0] == "bnez":
        # branch if reg is not equal to zero (could have been merged with bne but it is not implemented here)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        address = search_addr_by_label(line[2], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + mem_address_size

    elif line[0] == "fadd.d":
        # reg1 = reg2 + reg3  ~  fp
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0] == "fsqrt.d":
        # reg1 = sqrt(reg2)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]])

    elif line[0] == "bgt":
        # branch if reg1 is greater than reg2
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        address = search_addr_by_label(line[3], curr_address)
        write_bits(address)
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + mem_address_size

    elif line[0] == "fmv.s.x":
        # reg1 = reg2 (move from integer register to fp register)
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]])

    elif line[0] == "fmul.s":
        # reg1 = reg2 * reg3  ~  fp
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

    elif line[0] == "fadd.s":
        # reg1 = reg2 + reg3  ~  fp
        write_bits(opcode[line[0]])
        write_bits(reg_dict[line[1]])
        write_bits(reg_dict[line[2]])
        write_bits(reg_dict[line[3]])
        curr_address += len(opcode[line[0]]) + len(reg_dict[line[1]]) + len(reg_dict[line[2]]) + len(reg_dict[line[3]])

write_bits([0,0,0,0,0,0,0,0])   # write unwritten bits still in the stack
