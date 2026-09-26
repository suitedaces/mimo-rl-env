The `smt` dialect already has `smt.and`, `smt.or`, and `smt.xor` for the standard boolean connectives from the Core theory of the SMT-LIB 2.7 standard, but there's no operation for boolean implication (`=>`).

I'm lowering some verification conditions to the `smt` dialect and need to express things like "if `p` then `q`". Right now I have to expand it manually as `or(not(p), q)`, which is awkward and doesn't match what I'd write directly in SMT-LIB.

Could we get an `smt.implies` operation in the dialect with the same semantics as the `=>` operator from the SMT-LIB Core theory?
