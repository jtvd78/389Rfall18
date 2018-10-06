Writeup 5 - Binaries I
======

Name: Justin Van Dort  
Section: 0102

I pledge on my honor that I havie not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 5 Writeup

My first problem was finding out how the `System V` calling convention worked. Both the lecture slides
and Wikipedia said that integer and pointer arguments are passed in order in registers RDI, RSI, and RDX. 

I was originally going to implement the looping in `my_memcpy` via a comparing a counter with zero and then jumping
if they are equal. But, after reading `myfunc.S`, I realized there was a loop instruction that operated
on the counter register `rcx`. After getting the looping done, all I had to do was copy `val` to the 
destination address. Then, I needed to incremet the address by 1 byte. 

One mistake I made was writing `mov [rdi], rsi` intead of `mov [rdi] sil`. Before I was copying
4 bytes to the destination address. After the fix, I was only copying a single byte. 

For `my_strncpy`, I implemented looping in the same manner as `my_memcpy`. Incrementing the source
and destination registers were handled in the same way as `my_memcpy`, as well. The only difference is
that I needed to copy a value from memory to another memory location. First, I wrote `mov [rdi], [rsi]`,
but I quickly realized that did not work. So, I used the 1-byte `al` temporary register to store the byte 
from the source before I `mov`'d it to the destination. 