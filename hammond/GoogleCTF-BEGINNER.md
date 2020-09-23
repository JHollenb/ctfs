# BEGINNER
```
wget "thefile"
file beginner
mv beginner beginner.zip
unzip beginner.zip
chmod +x a.out
file a.out      // not-stripped means gdb symbols
```

## RECON
First lets look for a flag using strings:
```
strings a.out
ltrace a.out
strace a.out
```

## GHIDRA
Import executable
Debugging symbols haven't been stripped out, we can search for `main`
Rename `local_38` to `our_input`

`ctftime.org` - A lot of people were using `angr`

## `angr`
>`angr` is a python framework for analyzing binaries. It combines both static and dynamic symbolic ("concolic") analysis, making it applicable to a variety of tasks

Using `python 3.8.2`
```
python -m venv angr
ls angr/
source angr/bin/activate
python -m pip install angr
python
>>> import angr
>>> import claripy
```

```
import angr
import claripy

STDIN_FD = 0
success_addr = 0x0010111D
failure_addr = 0x00101100
base_addr    = 0x00100000
flag_length  = (16 - 1) # There is a null byte

proj = angr.Project("./a.out", main_opts = {"base_addr":base_addr})
flag_chars = [ claripy.BVS(f"flag_char{i}", 8) for i in range(flag_length) ] # build a flag string, byte-by-byte for the entire flag - flag_char0x1, flag_char0x2, ...
flag = claripy.Concat( *flag_chars + [claripy.BVV(b"\n")]) # So stdin works
state = proj.factory.full_init_state(
  args = [ "./a.out" ],
  add_options = angr.options.unicorn,
  stdin=flag
  )
  
for c in flag_chars:
  state.solver.add(c >= ord("!"))
  state.solver.add(c <= ord("~"))
  
sim_manager = proj.factory.simulation_manager(state)
sim_manager.explore(find=success_addr, avoid=failure_addr)
if (len(sim_manager.found) > 0):
  for found in sim_manager.found:
    print(found.posix.dumps(STDIN_FD))
```


Basically, this binary does some weird shuffling and we don't want to decrypt it ourselves. Let's use this tool.
# TAGS:Reverse-Engineering,Ghidra,
