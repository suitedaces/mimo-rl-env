## `Topology.from_pdb` fails on deprotonated cysteine (CYM)

I'm trying to load a protein PDB into an OpenFF `Topology` for parameterization. The structure has one cysteine where the side-chain thiol is deprotonated (i.e. the SG carries a negative charge and there's no HG). In our PDB files this residue is labelled `CYM`, which is the convention used by AMBER / tleap and a few other tools when they output structures with deprotonated cysteines (active sites, metal-coordinating cysteines, salt-bridged models, etc.).

What I'd expect is for `Topology.from_pdb` to handle this residue out of the box, the same way it handles the regular protonated `CYS` and the disulfide-bonded `CYX`.

What actually happens: the load fails on the CYM residue with an unassigned-chemistry error. If I rename / reprotonate that residue back to a normal `CYS` the same PDB loads without complaint, and all the other standard amino acids in the structure are fine — so the problem is specifically that the deprotonated cysteine isn't being recognized as a known residue.

A minimal repro is just an ACE-CYM-NME tripeptide (capped, single CYM in the middle, SG with no hydrogen attached, formal charge -1 on the sulfur), fed into `Topology.from_pdb`.

Deprotonated cysteine is common enough that I'd expect the built-in residue library to cover it, rather than every user having to hand-roll a `_custom_substructures` entry for what is essentially just a protonation state of an already-supported residue. Could `Topology.from_pdb` be taught to recognize CYM directly?
