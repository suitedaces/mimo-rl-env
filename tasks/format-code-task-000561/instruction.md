## Cannot force a sequence type when reading a FASTA file

When I load a FASTA file with `fasta.get_sequence(...)` / `fasta.get_sequences(...)` / `fasta.get_alignment(...)`, biotite always tries to guess the sequence type by first attempting to parse the string as a `NucleotideSequence` and falling back to `ProteinSequence` only when that fails.

This works most of the time, but it breaks for short protein sequences that happen to consist only of letters that are also valid nucleotide symbols. For example, a peptide like `ACGTACGT` or a fragment containing only residues from `{A, C, G, T, N}` will silently come back as a `NucleotideSequence`, even though the file clearly contains proteins.

```python
from biotite.sequence.io import fasta

f = fasta.FastaFile.read("my_proteins.fasta")
seq = fasta.get_sequence(f)
print(type(seq))  # NucleotideSequence -- but this is a protein file!
```

There is currently no way to tell these functions "this file contains proteins, don't guess". I have to bypass the convenience functions entirely and build the `ProteinSequence` objects manually from the raw strings, which also means re-implementing the small normalisations biotite does (uppercasing, handling `U`, etc.).

It would be very useful if `get_sequence`, `get_sequences` and `get_alignment` accepted an optional argument letting the caller specify the expected `Sequence` subclass up front. When provided, the auto-detection should be skipped and the given type used directly; when omitted, the current guessing behaviour should be preserved so existing code keeps working.

I'd expect to call it as a keyword argument, something like `seq_type=...`.
