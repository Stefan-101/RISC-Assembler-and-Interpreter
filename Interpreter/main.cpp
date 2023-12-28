#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdint>
#include <unordered_map>
#include <string>
#include <vector>
#include <variant>
using namespace std;

char buffer[8191];          // 8kB binary buffer

const int MEM_ADDR_SIZE = 16;
const int IMMEDIATE_SIZE = 32;

// FETCH FUNCTIONS prototypes

void (*fetchInstr())();
int64_t* fetchReg();
int32_t fetchImm();
int16_t fetchMemAddr();

// CPU REGISTERS
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

// INSTRUCTION FUNCTIONS
// all functions have the same signature even if not all parameters are used

void addi(){
    // reg1 = reg2 + 32-bits immediate (sign extended to 64 bits)
    cout << "SYS: addi has been called" << endl;
    int64_t* reg1 = fetchReg();
    int64_t* reg2 = fetchReg();
    int64_t imm = int64_t(fetchImm());
    *reg1 = *reg2 + imm;
}

void add(){
    // reg1 = reg2 + reg3
    cout << "SYS: add has been called" << endl;
    int64_t* reg1 = fetchReg();
    int64_t* reg2 = fetchReg();
    int64_t* reg3 = fetchReg();
    *reg1 = *reg2 + *reg3;
}

void j(){
    // sets instruction pointer to the memory address
    cout << "SYS: j has been called" << endl;
    reg.pc = int64_t(fetchMemAddr());
}

void ret(){
    // jump to the address in RA or end execution if RA is -1
    // TODO end execution if RA is -1
    cout << "SYS: ret has been called" << endl;
    reg.pc = reg.ra;

}

void li(){
    // reg1 = imm
    cout << "SYS: li has been called " << endl;
    int64_t* reg1 = fetchReg();
    *reg1 = int64_t(fetchImm());
}

void bge(){
    // branch if reg1 is greater than or equal to reg2
    cout << "SYS: bge has been called" << endl;
    int64_t* reg1 = fetchReg();
    int64_t* reg2 = fetchReg();
    int16_t mem_addr = fetchMemAddr();
    if (reg1 >= reg2)
        reg.pc = int64_t(mem_addr);
}

void beqz(){
    // branch if reg is equal to zero (could have been merged with beq but it is not implemented here)
    cout << "SYS: beqz has been called" << endl;
    int64_t* reg1 = fetchReg();
    int16_t mem_addr = fetchMemAddr();
    if (*reg1 == 0){
        cout << "SYS: BRANCH TRUE" << endl;
        reg.pc = int64_t(mem_addr);
    }
}

void fmv_s(){
    // copy fp reg2 in reg1 (could be merged with another instruction but it is not implemented here)
    // TODO fetch reg1, reg2
}

void sd(){
    // store 64 bits from reg to mem ~ e.g. sd reg1, 4(reg2)
    cout << "SYS: sd has been called " << endl;
    int64_t* reg1 = fetchReg();
    int16_t offset = fetchMemAddr();
    int64_t* reg2 = fetchReg();
    *reinterpret_cast<int64_t*>(&buffer[*reg2 + offset]) = *reg1;       // *reg2 + offset can be considered a virtual address
                                                                        // and &buffer[*reg2 + offset] its translation
}

void lb(){
    // load 8 bits from mem address, sign extend the value and store to reg
    cout << "SYS: lb has been called" << endl;
    int64_t* reg1 = fetchReg();
    int16_t offset = fetchMemAddr();
    int64_t* reg2 = fetchReg();
    *reg1 = int64_t(*reinterpret_cast<int8_t*>(&buffer[*reg2 + offset]));
}

void call(){
    // stores current pc and jumps to memory address (or executes a predefined function)
    uint16_t mem_addr = uint16_t(fetchMemAddr());
    char *start,*end;
    char scanf_buffer[1000];
    int i = 0;
    int scanf_buffer_index = 0;
    vector<int64_t*> regs = {&reg.a1, &reg.a2, &reg.a3, &reg.a4, &reg.a5, &reg.a6, &reg.a7};
    switch (mem_addr){
        // printf and scanf are simulated since we do not know during compilation how many args will be passed
        case 65535:
            cout << "SYS: branch printf was executed " << endl;
            // simulate printf function (only supports 7 args, stack reading not implemented here)
            start = &buffer[reg.a0];
            end = strchr(&buffer[reg.a0], '%');
            while (end){
                end[0] = '\0';
                cout << start;
                // only %d and %s are implemented here
                if (end[1] == 'd'){
                    cout << *regs.front();
                    regs.erase(regs.begin());
                }
                else if (end[1] == 's'){
                    cout << &buffer[*regs.front()];
                }
                start = &end[2];
                end = strchr(start,'%');
            }
            cout << start;
            
            break;
        case 65534:
            cout << "SYS: branch scanf was executed " << endl;
            // simulate scanf function (only supports 7 args, stack reading not implemented here)
            cin.getline(scanf_buffer,1000);
            while (scanf_buffer[scanf_buffer_index] != '\0' && buffer[reg.a0 + i] != '\0'){
                if (buffer[reg.a0 + i] == '%' && buffer[reg.a0 + i + 1] == 'd'){
                    //copy integer to mem address
                    *reinterpret_cast<int64_t*>(&buffer[*regs.front()]) = int64_t(atoi(&scanf_buffer[scanf_buffer_index]));
                    regs.erase(regs.begin());
                    while (scanf_buffer[scanf_buffer_index] >= '0' && scanf_buffer[scanf_buffer_index] <= '9')
                        scanf_buffer_index++;
                    i += 2;
                }
                else if (buffer[reg.a0 + i] == '%' && buffer[reg.a0 + i + 1] == 's'){
                    // copy string until first whitespace
                    char *start_cpy = &buffer[*regs.front()];
                    int cpy_index = 0;
                    while (!strchr("\n    ", scanf_buffer[scanf_buffer_index]))
                        start_cpy[cpy_index++] = scanf_buffer[scanf_buffer_index++];
                    
                    regs.erase(regs.begin());
                    i += 2;
                }
                else {
                    i++;
                    scanf_buffer_index++;
                }
            }

            break;
        case 65533:
            cout << "SYS: branch strlen was executed " << endl;
            reg.a0 = int64_t(strlen(&buffer[reg.a0]));
            break;
        default:
            cout << "SYS: branch default was executed" << endl;
            reg.ra = reg.pc;                    // save return address
            reg.pc = int64_t(mem_addr);         // jump to memory_address   
    }
}

void sb(){
    // store 8 bits from reg to mem
    cout << "SYS: sb has been called " << endl;
    int64_t* reg1 = fetchReg();
    int16_t offset = fetchMemAddr();
    int64_t* reg2 = fetchReg();
    *reinterpret_cast<int8_t*>(&buffer[*reg2 + offset]) = int8_t(*reg1 & 0xFF);
}

void lw(){
    // load 32 bits from mem address, sign extend the value and store to reg
    cout << "SYS: lw has been called" << endl;
    int64_t* reg1 = fetchReg();
    int16_t offset = fetchMemAddr();
    int64_t* reg2 = fetchReg();
    *reg1 = int64_t(*reinterpret_cast<int32_t*>(&buffer[*reg2 + offset]));
}

void ld(){
    // load 64 bits from mem address and store to reg
    cout << "SYS: ld has been called" << endl;
    int64_t* reg1 = fetchReg();
    int16_t offset = fetchMemAddr();
    int64_t* reg2 = fetchReg();
    *reg1 = *reinterpret_cast<int64_t*>(&buffer[*reg2 + offset]);
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
    cout << "SYS: la has been called" << endl;
    int64_t* reg1 = fetchReg();
    int16_t mem_addr = fetchMemAddr();
    *reg1 = int64_t(uint16_t(mem_addr)) / 8;    // transform bit address to byte address of variable in the buffer
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
    cout << "SYS: mul has been called" << endl;
    // reg1 = reg2 * reg3
    int64_t* reg1 = fetchReg();
    int64_t* reg2 = fetchReg();
    int64_t* reg3 = fetchReg();
    *reg1 = *reg2 * *reg3;
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
    {"1011", reinterpret_cast<int64_t*>(&reg.ft0)},         // these are reinterpreted to make the lookup
    {"0101", reinterpret_cast<int64_t*>(&reg.ft1)},         // table easier to work with
    {"10010111", reinterpret_cast<int64_t*>(&reg.ft2)},
    {"1001010", reinterpret_cast<int64_t*>(&reg.ft3)},
    {"00000", reinterpret_cast<int64_t*>(&reg.fa0)},
    {"000011", reinterpret_cast<int64_t*>(&reg.fa1)},
    {"100100", reinterpret_cast<int64_t*>(&reg.fa2)}
};

// FETCH FUNCTIONS

// fetch instruction
void (*fetchInstr())(){
    string opcode = "";
    while (opcode_map.find(opcode) == opcode_map.end()){
        // continue reading bits and searching for an opcode
        opcode += to_string((buffer[reg.pc/8] >> (7 - reg.pc % 8)) & 1);
        reg.pc++;
    }
    return opcode_map.find(opcode) -> second;
}

// fetch register
int64_t* fetchReg(){
    string opcode = "";
    while (reg_map.find(opcode) == reg_map.end()){
        opcode += to_string((buffer[reg.pc/8] >> (7 - reg.pc % 8)) & 1);
        reg.pc++;
    }
    return reg_map.find(opcode) -> second;
}

int32_t fetchImm(){
    int32_t immediate = 0;
    for (int bits_cnt = 0; bits_cnt < 32; bits_cnt++){
        immediate <<= 1;
        immediate |= (buffer[reg.pc/8] >> (7 - reg.pc % 8)) & 1;
        reg.pc++;
    }
    return immediate;
}

int16_t fetchMemAddr(){
    int16_t mem_addr = 0;
    for (int bits_cnt = 0; bits_cnt < 16; bits_cnt++){
        mem_addr <<= 1;
        mem_addr |= (buffer[reg.pc/8] >> (7 - reg.pc % 8)) & 1;
        reg.pc++;
    }
    return mem_addr;
}

int main(){
    // I/O files
    char executable_file[] = "test.o";
    char stateIn[] = "blank_file.in";
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
    //tests
    for (int i = 0; i < 7; i++){
        fetchInstr()();
    }
 


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
// TODO conditional console SYS messages