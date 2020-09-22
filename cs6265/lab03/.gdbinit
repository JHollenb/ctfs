set disassembly-flavor intel

define hookpost-file
set sysroot /
end

define init-pwndbg
source /home/bin/pwndbg-git/gdbinit.py
end
document init-pwndbg
Initializes PwnDBG
end