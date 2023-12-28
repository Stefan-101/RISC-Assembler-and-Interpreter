.section .rodata
enter_prompt: .asciz "Enter a, b, and c: "
scan: .asciz "%s %s %d"
result_out: .asciz "Result = %d\n"

.section .text
.global main
main:
    addi    sp, sp, -32     # Allocate 32 bytes from the stack
    sd      ra, 0(sp)       # Since we are making calls, we need the original ra

    la a0,scan
    addi a1,sp,8
    addi a2,sp,16
    addi a3,sp,24
    call scanf
    addi    sp, sp, 32       # Always deallocate the stack!
    ret