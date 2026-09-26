## `arith` interpreter is missing several common signed integer ops

I'm running some IR through the xdsl interpreter as part of testing my compiler pipeline. As soon as my programs do anything beyond the basics, the interpreter fails because the relevant op has no implementation registered.

Concretely, `ArithFunctions` currently only covers add / sub / mul (and `cmpi` + a couple of float ops). Anything that involves bit shifts, signed integer division, or signed remainder isn't supported, so a program like

```
%shift = arith.shli %a, %b : i32
%q     = arith.divsi %x, %y : i32
%r     = arith.remsi %x, %y : i32
```

can't actually be executed — the interpreter just errors out on the first such op.

Could the rest of the basic signed integer arithmetic from the `arith` dialect be wired up in the interpreter? Without shifts and signed division/remainder it's pretty hard to run anything non-trivial end to end. The semantics should just match what these ops mean in MLIR.
