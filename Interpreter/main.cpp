#include <iostream>
#include <fstream>
#include <cstdint>
#include <unordered_map>
#include <string>
using namespace std;

char buffer[8191];          // 8kB binary buffer
char current_byte;          // the current byte that is being worked on
int current_byte_length;    

const int MEM_ADDR_SIZE = 16;
const int IMMEDIATE_SIZE = 32;

// CPU REGISTERS
struct{
    int64_t pc = 0;     // program counter

    int64_t t0;
    int64_t t1;
    int64_t a0;
    int64_t sp = 8192;  // empty stack
    int64_t ft0;
    int64_t a1;
    int64_t t3;
    int64_t ft1;
    int64_t t2;
    int64_t t4;
    int64_t a2;
    int64_t fa0;
    int64_t t5;
    int64_t s1;
    int64_t fa2;
    int64_t fa1;
    int64_t ra;
    int64_t ft3;
    int64_t ft2;
    int64_t zero = 0;       // should be constant but it's easier to work if they all have the same data type
    int64_t a3;
    int64_t ft11;
    int64_t ft10;
    int64_t ft9;
    int64_t ft8;
    int64_t fs11;
    int64_t fs10;
    int64_t fs9;
    int64_t fs8;
    int64_t fs7;
    int64_t fs6;
    int64_t fs5;
    int64_t fs4;
    int64_t fs3;
    int64_t fs2;
    int64_t fa7;
    int64_t fa6;
    int64_t fa5;
    int64_t fa4;
    int64_t fa3;
    int64_t fs1;
    int64_t fs0;
    int64_t ft7;
    int64_t ft6;
    int64_t ft5;
    int64_t ft4;
    int64_t t6;
    int64_t s11;
    int64_t s10;
    int64_t s9;
    int64_t s8;
    int64_t s7;
    int64_t s6;
    int64_t s5;
    int64_t s4;
    int64_t s3;
    int64_t s2;
    int64_t a7;
    int64_t a6;
    int64_t a5;
    int64_t a4;
    int64_t s0;
    int64_t tp;
    int64_t gp;
}reg;

// INSTRUCTION FUNCTIONS
// all functions have the same signature even if not all parameters are used

void addi(){
    // reg1 = reg2 + 32-bits immediate (sign extended to 64 bits)
    // TODO fetch REG1, REG2, IMM
    // test
    cout << "addi was called" << endl;
}

void add(){
    // reg1 = reg2 + reg3
    // TODO fetch REG1, REG2, REG3
}

void j(){
    // sets instruction pointer to the memory address
    //TODO fetch MEM_ADDR
}

void ret(){
    // jump to the address in RA
    reg.pc = reg.ra;
}

void li(){
    // reg1 = imm
    // TODO fetch reg1 and imm
}

void bge(){
    // branch if reg1 is greater than or equal to reg2
    // TODO fetch reg1, reg2, mem_addr
}

void beqz(){
    // branch if reg is equal to zero (could have been merged with beq but it is not implemented here)
    // TODO fetch reg1, mem_addr
}

void fmv_s(){
    // copy fp reg2 in reg1 (could be merged with another instruction but it is not implemented here)
    // TODO fetch reg1, reg2
}

void sd(){
    // store 64 bits from reg to mem ~ sd reg1, 4(reg2)
    // TODO fetch reg1, reg2, offset
    cout << "sd has been called" << endl;
}

void lb(){
    // load 8 bits from mem address, sign extend the value and store to reg
    // TODO fetch reg1, reg2 offset
}

void call(){
    // stores current ip + call_size + mem_addr_size and jumps to mem addr
    // TODO fetch mem_addr (there are also predefined jumps)
}

void sb(){
    // store 8 bits from reg to mem
    // TODO fetch reg1, reg2, offset
}

void lw(){
    // load 32 bits from mem address, sign extend the value and store to reg
    // TODO fetch reg1, reg2, offset
}

void ld(){
    // load 64 bits from mem address and store to reg
    // TODO fetch reg1, reg2, offset
}

void flt_s(){
    // reg1 = reg2 < reg3    (boolean result)
    // TODO fetch reg1, reg2, reg3
}

void fld(){
    // load 64 bits from mem address and store to reg (fp)
    // TODO fetch reg1, reg2, offset
}

void la(){
    // load address in register
    // TODO fetch reg1, mem_addr
    cout << "la has been called" << endl;
}

void fsw(){
    // store 32 bit fp to memory address
    // TODO fetch reg1, reg2, offset
}

void slli(){
    // logical left shift on reg2 by amount held in immediate and store to reg1
    // immediate is an unsigned 6 bit value
    // TODO fetch reg1, reg2, imm
}

void flw(){
    return;
}

void srai(){
    return;
}

void fmul_d(){
    return;
}

void fsub_d(){
    return;
}

void fsqrt_d(){
    return;
}

void fadd_d(){
    return;
}

void fmv_s_x(){
    return;
}

void bgt(){
    return;
}

void bnez(){
    return;
}

void sub(){
    return;
}

void fadd_s(){
    return;
}

void fmul_s(){
    return;
}

void mul(){
    return;
}

unordered_map<string, void(*)()> opcode_map = {
    // lookup table used to decode huffman codes
    // keys are string to make decoding easier

    {"110",  &addi},
    {"001",  &add},
    {"1111",  &j},
    {"1011",  &ret},
    {"1010",  &li},
    {"1000",  &bge},
    {"11101",  &beqz},
    {"11100",  &fmv_s},
    {"10011",  &sd},
    {"01111",  &lb},
    {"01101",  &call},
    {"01100",  &sb},
    {"01011",  &lw},
    {"01010",  &ld},
    {"00011",  &flt_s},
    {"00010",  &fld},
    {"100101",  &la},
    {"100100",  &fsw},
    {"011101",  &slli},
    {"011100",  &flw},
    {"010001",  &srai},
    {"000011",  &fmul_d},
    {"000010",  &fsub_d},
    {"0100111",  &fsqrt_d},
    {"0100110",  &fadd_d},
    {"0100101",  &fmv_s_x},
    {"0100100",  &bgt},
    {"0100001",  &bnez},
    {"0100000",  &sub},
    {"0000011",  &fadd_s},
    {"0000010",  &fmul_s},
    {"000000",  &mul}
};

unordered_map<string, int64_t*> reg_map = {
    // lookup table used to decode huffman codes
    // keys are string to make decoding easier

    {"0001", &reg.zero},
    {"000010", &reg.ra},
    {"1100", &reg.sp},
    {"111", &reg.t0},
    {"011", &reg.t1},
    {"0100", &reg.t2},
    {"100110", &reg.s1},
    {"001", &reg.a0},
    {"1010", &reg.a1},
    {"11010", &reg.a2},
    {"100101101", &reg.a3},
    {"1000", &reg.t3},
    {"11011", &reg.t4},
    {"100111", &reg.t5},
    {"1011", &reg.ft0},
    {"0101", &reg.ft1},
    {"10010111", &reg.ft2},
    {"1001010", &reg.ft3},
    {"00000", &reg.fa0},
    {"000011", &reg.fa1},
    {"100100", &reg.fa2}
};

// FETCH FUNCTIONS

// fetch instruction
void (*fetchInstr())(){
    string opcode = "";
    while (opcode_map.find(opcode) == opcode_map.end()){
        // continue reading bits and searching for an opcode
        if (!current_byte_length){
            current_byte = buffer[reg.pc/8];
            current_byte_length = 8;
        }
        opcode += to_string((current_byte >> 7) & 1);
        current_byte <<= 1; current_byte_length--;
        reg.pc++;
    }
    return opcode_map.find(opcode) -> second;
}

// fetch register
int64_t* fetchReg(){
    string opcode = "";
    while (reg_map.find(opcode) == reg_map.end()){
        if (!current_byte_length){
            current_byte = buffer[reg.pc/8];
            current_byte_length = 8;
        }
        opcode += to_string((current_byte >> 7) & 1);
        current_byte <<= 1; current_byte_length--;
        reg.pc++;
    }
    return reg_map.find(opcode) -> second;
}

int32_t fetchImm(){
    int32_t immediate = 0;
    for (int bits_cnt = 0; bits_cnt < 32; bits_cnt++){
        if (!current_byte_length){
            current_byte = buffer[reg.pc/8];
            current_byte_length = 8;
        }
        immediate <<= 1;
        immediate |= (current_byte >> 7) & 1;
        current_byte <<= 1; current_byte_length--;

        reg.pc++;
    }
    return immediate;
}

int16_t fetchMemAddr(){
    int16_t mem_addr = 0;
    for (int bits_cnt = 0; bits_cnt < 16; bits_cnt++){
        if (!current_byte_length){
            current_byte = buffer[reg.pc/8];
            current_byte_length = 8;
        }
        mem_addr <<= 1;
        mem_addr |= (current_byte >> 7) & 1;
        current_byte <<= 1; current_byte_length--;

        reg.pc++;
    }
    return mem_addr;
}

int main(){
    // I/O files
    char executable_file[] = "func_10";
    char stateIn[] = "file.out";
    char stateOut[] = "file.out";



    // LOAD STATE
    // load registers and memory in buffer

    ifstream stateFileIn(stateIn, ios::binary);

    stateFileIn.read(reinterpret_cast<char*>(&reg), sizeof(reg));

    // we can use the stack pointer to calculate where to load the rest of the memory from the state file

    stateFileIn.read(&buffer[reg.sp], 8191 - reg.sp + 1);

    stateFileIn.close();



    // LOAD EXECUTABLE
    // load entry point from binary file

    ifstream bin_exec(executable_file, ios::binary);

    int16_t entryPoint;
    bin_exec.read(reinterpret_cast<char*>(&entryPoint), sizeof(entryPoint));
    reg.pc = int64_t(entryPoint);

    // load the rest of the file in buffer starting at position 0

    bin_exec.seekg(0, ios::end);
    streampos fileSize = bin_exec.tellg();
    streampos bytesReadSoFar = sizeof(entryPoint);
    streampos remainingSize = fileSize - bytesReadSoFar;
    bin_exec.seekg(bytesReadSoFar, ios::beg);
    bin_exec.read(buffer, remainingSize);

    bin_exec.close();



    // EXECUTE INSTRUCTIONS
    // tests
    reg.pc = int64_t(24);
    current_byte = buffer[reg.pc/8];
    fetchInstr()();
    fetchReg();
    fetchReg();
    cout << fetchImm() << endl;
    fetchInstr()();
    fetchReg();
    cout << int(fetchMemAddr()) << endl;
    fetchReg();
    fetchInstr()();
    fetchReg();
    cout << fetchMemAddr() << endl;
    


    // STORE STATE
    // output registers and memory from buffer
    // since our functions do not use variables (only constants) and there are no heap allocations,
    // file.out will contain registers and the stack

    ofstream stateFileOut(stateOut, ios::binary);

    // write registers state
    stateFileOut.write(reinterpret_cast<char*>(&reg), sizeof(reg));

    // write the stack
    stateFileOut.write(&buffer[reg.sp], 8191 - reg.sp + 1);      // stack_size = 8191 - reg.sp + 1

    stateFileOut.close();
    
    return 0;
}

// TODO check file opens