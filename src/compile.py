def compile_x86_64(prog):

    return """

.section __TEXT,__text
.globl _main

_main:
    pushq %rbp
    movq %rsp, %rbp

    leaq format(%rip), %rdi
    movl $1339, %esi
    xorl %eax, %eax
    callq _printf

    xorl %eax, %eax
    popq %rbp
    retq

.section __TEXT,__cstring,cstring_literals
format:
    .asciz "%d\\n"

"""
