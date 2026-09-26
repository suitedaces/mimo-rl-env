## `ao` doesn't let me filter the ESIL expression of an opcode by output

When I'm reversing something, I quite often want to look at the ESIL
representation of a single instruction — `aoe` already does that nicely.
But for most non-trivial instructions the ESIL expression touches several
things at once: a destination register, the stack pointer, and a handful
of flags (`zf`, `cf`, `sf`, …). The whole thing comes out as one long
chained expression.

What I actually want, most of the time, is just the slice of that
expression that produces **one specific output** — e.g. "show me only the
part of this instruction's ESIL that determines `zf`", or "show me only
the part that ends up in `rax`". Right now I have to read the full ESIL
expression and mentally project out the sub-computation that feeds the
output I care about, which is annoying for anything more complex than a
plain `mov`.

I noticed that radare2 already has the machinery for this on the ESIL /
DFG side — there is filtering by output expression available there — but
it doesn't seem to be exposed from the `ao` family of commands. From a
workflow point of view it would be much more natural to ask for it
directly at the opcode level: stand on an instruction, ask `ao` for the
ESIL slice corresponding to some output expression, get back just that
slice.

Could `ao` grow a subcommand that takes an output expression as argument
and prints the filtered ESIL expression for the instruction at the
current offset? It should also show up in `ao?` help so it's discoverable
next to `aoe`. I'd expect to invoke it as something like `aof <expr>`.
