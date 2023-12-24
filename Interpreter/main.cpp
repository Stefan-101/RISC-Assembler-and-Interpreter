#include <iostream>
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
    int64_t sp;
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

void addi(int64_t* REG1, int64_t* REG2, int64_t* /*unused*/, int32_t IMM){
    return;
}

void add(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void j(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void ret(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void li(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void bge(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void beqz(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fmv_s(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void sd(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void lb(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void call(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void sb(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void lw(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void ld(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void flt_s(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fld(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void la(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fsw(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void slli(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void flw(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void srai(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fmul_d(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fsub_d(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fsqrt_d(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fadd_d(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fmv_s_x(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void bgt(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void bnez(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void sub(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fadd_s(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void fmul_s(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

void mul(int64_t* REG1, int64_t* REG2, int64_t* REG3, int32_t IMM){
    return;
}

unordered_map<uint8_t, void(*)(int64_t*, int64_t*, int64_t*, int32_t)> opcode_map = {
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

    // load entry point from binary file

    // TODO ...

    // load binary file in memory buffer starting at 0

    // TODO ...

    // load registers and memory from file.in in buffer starting at ??

    // TODO ...

    // Execute the instructions

    // TODO ...

    // output registers and memory from buffer in file.out

    // TODO ...

    return 0;
}