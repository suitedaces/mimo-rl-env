## `HBondAcceptorCountDescriptor` undercounts carbonyl oxygens attached to aromatic rings

I'm using `HBondAcceptorCountDescriptor` to compute `nHBAcc` for a screening set and noticed it gives 0 for molecules that obviously have a hydrogen-bond-accepting carbonyl, as long as the carbonyl carbon happens to be part of an aromatic ring.

Minimal example — acetophenone (`CC(=O)c1ccccc1`):

```java
IAtomContainer mol = new SmilesParser(SilentChemObjectBuilder.getInstance())
        .parseSmiles("CC(=O)c1ccccc1");

HBondAcceptorCountDescriptor d = new HBondAcceptorCountDescriptor();
d.setParameters(new Object[]{ true });   // checkAromaticity
DescriptorValue v = d.calculate(mol);
System.out.println(v.getValue());        // -> 0
```

I'd expect the carbonyl oxygen to be counted, so `nHBAcc = 1`. Same story for things like benzaldehyde, methyl benzoate, or 4-pyridone — the C=O oxygen is a textbook H-bond acceptor but the descriptor returns 0.

Looking at the descriptor's own javadoc, the intent for oxygen seems to be:

> any oxygen with formal charge ≤ 0, **except**
> 1. an aromatic ether oxygen (an ether oxygen adjacent to an aromatic carbon)
> 2. an oxygen adjacent to a nitrogen

So aromatic *ether* oxygens (like the ring O in furan, or an –O– bridging into a phenyl) should be excluded — that part is fine. But a carbonyl O that just happens to be doubly bonded to an aromatic-ring carbon isn't an ether oxygen at all and shouldn't fall under that exclusion.

Right now the descriptor seems to treat any O adjacent to an aromatic C the same way, so all aromatic carbonyls (ketones, aldehydes, amides, esters fused to aromatic rings, pyridone-type tautomers, …) silently get dropped from the count. Could the oxygen rule be tightened so that only the aromatic-ether case is excluded, and aromatic-ring carbonyl oxygens are counted as acceptors like the docs imply?
