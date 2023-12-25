#include <iostream>
#include <fstream>
#include <cstdint>
#include <unordered_map>
using namespace std;

char buffer[8191];  // 8kB binary buffer

// CPU REGISTERS
struct{
    int64_t ip = 0;     // instruction pointer

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
    reg.ip = reg.ra;
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

unordered_map<uint8_t, void(*)()> opcode_map = {
    // lookup table used to decode huffman codes
    // codes are padded with set bits to the left

    {254,  &addi},
    {249,  &add},
    {255,  &j},
    {251,  &ret},
    {250,  &li},
    {248,  &bge},
    {253,  &beqz},
    {252,  &fmv_s},
    {243,  &sd},
    {239,  &lb},
    {237,  &call},
    {236,  &sb},
    {235,  &lw},
    {234,  &ld},
    {227,  &flt_s},
    {226,  &fld},
    {229,  &la},
    {228,  &fsw},
    {221,  &slli},
    {220,  &flw},
    {209,  &srai},
    {195,  &fmul_d},
    {194,  &fsub_d},
    {167,  &fsqrt_d},
    {166,  &fadd_d},
    {165,  &fmv_s_x},
    {164,  &bgt},
    {161,  &bnez},
    {160,  &sub},
    {131,  &fadd_s},
    {130,  &fmul_s},
    {192,  &mul}
};

unordered_map<uint32_t, int64_t*> reg_map = {
    // lookup table used to decode huffman codes
    // codes are padded with set bits to the left

    {4294967288, &reg.zero},
    {4294967248, &reg.ra},
    {4294967283, &reg.sp},
    {4294967295, &reg.t0},
    {4294967294, &reg.t1},
    {4294967282, &reg.t2},
    {4294967257, &reg.s1},
    {4294967292, &reg.a0},
    {4294967285, &reg.a1},
    {4294967275, &reg.a2},
    {4294967145, &reg.a3},
    {4294967281, &reg.t3},
    {4294967291, &reg.t4},
    {4294967289, &reg.t5},
    {4294967293, &reg.ft0},
    {4294967290, &reg.ft1},
    {4294967273, &reg.ft2},
    {4294967209, &reg.ft3},
    {4294967264, &reg.fa0},
    {4294967280, &reg.fa1},
    {4294967241, &reg.fa2}
};

int main(){
    // I/O files
    char executable_file[] = "func_10";
    char stateIn[] = "file.in";
    char stateOut[] = "file.out";



    // LOAD EXECUTABLE
    // load entry point from binary file

    ifstream bin_exec(executable_file, ios::binary);

    int16_t value;
    bin_exec.read(reinterpret_cast<char*>(&reg.ip), sizeof(value));
    reg.ip = int64_t(value);

    // load the rest of the file in buffer starting at position 0

    bin_exec.seekg(0, ios::end);
    streampos fileSize = bin_exec.tellg();
    streampos bytesReadSoFar = sizeof(value);
    streampos remainingSize = fileSize - bytesReadSoFar;
    bin_exec.seekg(bytesReadSoFar, ios::beg);
    bin_exec.read(buffer, remainingSize);

    bin_exec.close();



    // LOAD STATE
    // load registers and memory in buffer

    ifstream stateFileIn(stateIn, ios::binary);

    stateFileIn.read(reinterpret_cast<char*>(&reg), sizeof(reg));

    // we can use the stack pointer to calculate where to load the rest of the memory from the state file

    stateFileIn.read(&buffer[reg.sp], 8191 - reg.sp + 1);

    stateFileIn.close();



    // EXECUTE INSTRUCTIONS

    // TODO ...




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