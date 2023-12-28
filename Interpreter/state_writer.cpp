// *Rudimentary* state file reader
//
// Outputs a human readable txt file from a .in/.out state file
//
// Compiled with: g++ version 13.1.0
//
// Run: ./state_reader.exe <bin_file_in> <txt_file_out>

#include <iostream>
#include <cstring>
#include <cstdint>
#include <fstream>
using namespace std;

char buffer[8191];

struct{
    int64_t pc = 0;     // program counter ~ points to bit address within the buffer
    int64_t t0;
    int64_t t1;
    int64_t a0;
    int64_t sp = 8192;  // empty stack ~ points to byte address within the buffer
    double ft0;
    int64_t a1;
    int64_t t3;
    double ft1;
    int64_t t2;
    int64_t t4;
    int64_t a2;
    double fa0;
    int64_t t5;
    int64_t s1;
    double fa2;
    double fa1;
    int64_t ra;
    double ft3;
    double ft2;
    int64_t zero = 0;       // should be constant but it's easier to work if they all have the same data type
    int64_t a3;
    double ft11;
    double ft10;
    double ft9;
    double ft8;
    double fs11;
    double fs10;
    double fs9;
    double fs8;
    double fs7;
    double fs6;
    double fs5;
    double fs4;
    double fs3;
    double fs2;
    double fa7;
    double fa6;
    double fa5;
    double fa4;
    double fa3;
    double fs1;
    double fs0;
    double ft7;
    double ft6;
    double ft5;
    double ft4;
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

int main(int argc, char* argv[]){
    // load state file
    char stateIn[] = "blank_file.in";
    char stateOut[] = "file.in";
    ifstream stateFileIn(stateIn, ios::binary);
    ofstream output(stateOut);

    stateFileIn.read(reinterpret_cast<char*>(&reg), sizeof(reg));

    // we can use the stack pointer to calculate where to load the rest of the memory from the state file

    stateFileIn.read(&buffer[reg.sp], 8191 - reg.sp + 1);

    stateFileIn.close();

    // EDIT regs

    reg.sp -= 100;
    strcpy(&buffer[reg.sp], "Copy n bytes from here!");
    reg.a0 = reg.sp + 30;
    reg.a1 = reg.sp;
    reg.a2 = 4;

    // STORE STATE
    // since our functions do not use variables (only constants) and there are no heap allocations,
    // file.out will contain registers and the stack

    ofstream stateFileOut(stateOut, ios::binary);

    if (!stateFileOut.is_open()){
        cout << "stateFileOut could not be oppened";
        return 0;
    }

    // write registers state
    stateFileOut.write(reinterpret_cast<char*>(&reg), sizeof(reg));

    // write the stack
    stateFileOut.write(&buffer[reg.sp], 8191 - reg.sp + 1);      // stack_size = 8191 - reg.sp + 1

    stateFileOut.close();
    
    return 0;

    return 0;
}