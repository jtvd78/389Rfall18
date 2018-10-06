section .text         ;declare this section to include executable instructions

global my_memset      ;export the 'my_memset' symbol to be accessible outside of file
my_memset:
        push rbp      ;saves the base pointer for the previous function's stack frame
        mov rbp, rsp  ;moves up the base pointer to the top of the stack to create a new frame

        ; RDI is first arg (char *str)
        ; RSI is second arg  (char val)
        ; RDX is third arg (inst strl)

        mov rcx, rdx ;move the input argument from rdx to the counter register rcx

mem_loop:

        mov [rdi], sil          ; Set character at string pointer to 'val'.
        add rdi, 1              ; Increment string pointer.
        loop mem_loop           ; Continue loop until rcx == 0. 

        leave         ;moves down the stack pointer to the current base pointer,
                      ;and restores our saved base pointer, effectively
                      ;restoring our previous stack frame
        ret           ;jumps to the top value on the stack, hopefully the return address!


global my_strncpy     ;export the 'my_strncpy' symbol to be accessible outside of file
my_strncpy:
        push rbp      ;saves the base pointer for the previous function's stack frame
        mov rbp, rsp  ;moves up the base pointer to the top of the stack to create a new frame

        ; RDI is first arg (char *dst)
        ; RSI is second arg  (char *src)
        ; RDX is third arg (ins len)

        mov rcx, rdx ;move the input argument from rdx to the counter register rcx

str_loop:

        mov al, [rsi]           ; Copy source character to 'al' from source address.
        mov [rdi], al           ; Copy source character to destination address.

        add rdi, 1              ; Increment dst pointer.
        add rsi, 1              ; Increment src pointer.

        loop str_loop           ; Continue loop until rcx == 0. 

        leave         ;moves down the stack pointer to the current base pointer,
                      ;and restores our saved base pointer, effectively
                      ;restoring our previous stack frame
        ret           ;jumps to the top value on the stack, hopefully the return address!
