# RISC-Assembler-and-Interpreter  
__Assembler__  
Running the assembler:  
```python3.11 main.py <source_code> <objFiles> <output>```  
  
Binary values are big-endian except for the entry point address (first 2B at the start of the output file).  
Source code from .s files (along with the .o file for function 10) are assembled in binary files without extension.  
  
__Interpreter__  
Compiled with g++ 13.1.0 ~ optimization O2.
  
Running the interpreter:  
```./main.exe <executable_bin_file> <state.in> <state.out>```  
  
Each function has a folder where you can find:  
* a binary executable without an extension  
* binary state files .in/.out for registers and memory  
* translation for .in/.out files in .txt format (using state_reader.cpp) along with comments for relevant values from memory  
  
### Assembler references  
**__RISC-V instructions behaviour__**:  
https://msyksphinz-self.github.io/riscv-isadoc/  
https://marz.utk.edu/my-courses/cosc230/book/instructing-the-cpu/  
https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf  
**__Creating an ISA, transforming text to ISA__**:  
https://www.youtube.com/watch?v=wjHlvQfo5uI (our assembler has variable length instructions)  
https://www.youtube.com/watch?v=5ImTvOyvH2w    
  
### Interpreter references  
**__Function pointers__**:  
https://manderc.com/types/functionpointertype/index_eng.php  
**__Lookup tables__**:  
https://stackoverflow.com/questions/51624933/how-exactly-do-lookup-tables-work-and-how-to-implement-them  
https://en.cppreference.com/w/cpp/container/unordered_map  
**__Writing to a binary file__**:  
https://stackoverflow.com/questions/9244563/writing-integer-to-binary-file-using-c  
**__Implementing instruction behaviour__**:  
https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf  
**__State machine__**:  
https://cs.unibuc.ro/~crusu/asc/Arhitectura%20Sistemelor%20de%20Calcul%20(ASC)%20-%20Curs%200x05.pdf  (Slides 9-16)
  
### RISC-V source code
https://marz.utk.edu/my-courses/cosc230/book/example-risc-v-assembly-programs/  
