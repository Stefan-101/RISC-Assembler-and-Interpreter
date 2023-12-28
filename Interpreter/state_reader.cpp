// Rudimentary state file reader
// Outputs a human readable txt file from a .in/.out state file
// Compiled with: g++ version 13.1.0
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
    char stateIn[100];
    char readableOutputFile[100];
    strcpy(stateIn,argv[1]);
    strcpy(readableOutputFile,argv[2]);
    ifstream stateFileIn(stateIn, ios::binary);
    ofstream output(readableOutputFile);

    stateFileIn.read(reinterpret_cast<char*>(&reg), sizeof(reg));

    // we can use the stack pointer to calculate where to load the rest of the memory from the state file

    stateFileIn.read(&buffer[reg.sp], 8191 - reg.sp + 1);

    stateFileIn.close();

    // output regs
    output << "REGISTERS" << endl;
    output << "pc: " << reg.pc << endl;
    output << "t0: " << reg.t0 << endl;
    output << "t1: " << reg.t1 << endl;
    output << "a0: " << reg.a0 << endl;
    output << "sp: " << reg.sp << endl;
    output << "ft0: " << reg.ft0 << endl;
    output << "a1: " << reg.a1 << endl;
    output << "t3: " << reg.t3 << endl;
    output << "ft1: " << reg.ft1 << endl;
    output << "t2: " << reg.t2 << endl;
    output << "t4: " << reg.t4 << endl;
    output << "a2: " << reg.a2 << endl;
    output << "fa0: " << reg.fa0 << endl;
    output << "t5: " << reg.t5 << endl;
    output << "s1: " << reg.s1 << endl;
    output << "fa2: " << reg.fa2 << endl;
    output << "fa1: " << reg.fa1 << endl;
    output << "ra: " << reg.ra << endl;
    output << "ft3: " << reg.ft3 << endl;
    output << "ft2: " << reg.ft2 << endl;
    output << "zer: " << reg.zero << endl;
    output << "a3: " << reg.a3 << endl;
    output << "ft11: " << reg.ft11 << endl;
    output << "ft10: " << reg.ft10 << endl;
    output << "ft9: " << reg.ft9 << endl;
    output << "ft8: " << reg.ft8 << endl;
    output << "fs11: " << reg.fs11 << endl;
    output << "fs10: " << reg.fs10 << endl;
    output << "fs9: " << reg.fs9 << endl;
    output << "fs8: " << reg.fs8 << endl;
    output << "fs7: " << reg.fs7 << endl;
    output << "fs6: " << reg.fs6 << endl;
    output << "fs5: " << reg.fs5 << endl;
    output << "fs4: " << reg.fs4 << endl;
    output << "fs3: " << reg.fs3 << endl;
    output << "fs2: " << reg.fs2 << endl;
    output << "fa7: " << reg.fa7 << endl;
    output << "fa6: " << reg.fa6 << endl;
    output << "fa5: " << reg.fa5 << endl;
    output << "fa4: " << reg.fa4 << endl;
    output << "fa3: " << reg.fa3 << endl;
    output << "fs1: " << reg.fs1 << endl;
    output << "fs0: " << reg.fs0 << endl;
    output << "ft7: " << reg.ft7 << endl;
    output << "ft6: " << reg.ft6 << endl;
    output << "ft5: " << reg.ft5 << endl;
    output << "ft4: " << reg.ft4 << endl;
    output << "t6: " << reg.t6 << endl;
    output << "s11: " << reg.s11 << endl;
    output << "s10: " << reg.s10 << endl;
    output << "s9: " << reg.s9 << endl;
    output << "s8: " << reg.s8 << endl;
    output << "s7: " << reg.s7 << endl;
    output << "s6: " << reg.s6 << endl;
    output << "s5: " << reg.s5 << endl;
    output << "s4: " << reg.s4 << endl;
    output << "s3: " << reg.s3 << endl;
    output << "s2: " << reg.s2 << endl;
    output << "a7: " << reg.a7 << endl;
    output << "a6: " << reg.a6 << endl;
    output << "a5: " << reg.a5 << endl;
    output << "a4: " << reg.a4 << endl;
    output << "s0: " << reg.s0 << endl;
    output << "tp: " << reg.tp << endl;
    output << "gp: " << reg.gp << endl;
    output << endl << "STACK" << endl;

    for (int i = reg.sp; i < 8192; i++){
        output << i << ": 0x" << hex << int32_t(buffer[i]) << dec << " (" << int32_t(buffer[i]) << ") ";
        if (buffer[i] < 128){
            switch (buffer[i]){
                case ' ':
                    output << "[SPACE]" << endl;
                    break;
                case '\0':
                    output << "[NULL]" << endl;
                    break;
                case '\n':
                    output << "[ENTER]" << endl;
                    break;
                default:
                    output << buffer[i] << endl;
                    break;
            }
        }
        else output << endl;
    }

    stateFileIn.close();
    output.close();

    return 0;
}