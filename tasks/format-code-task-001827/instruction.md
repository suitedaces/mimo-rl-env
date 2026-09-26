## Add a built-in `Smiles` key maker (alongside `Inchi` / `InchiKey`)

When using `MoleculeJsonizer` / `MoleculeMongoDb`, stk ships ready-to-use key makers for InChI and InChIKey:

```python
import stk

jsonizer = stk.MoleculeJsonizer(
    key_makers=(stk.Inchi(), stk.InchiKey()),
)
```

SMILES is at least as common as InChI/InChIKey for indexing and querying molecules, but there is no equivalent `stk.Smiles()` — every project has to roll its own. Following the recipe in the `MoleculeMongoDb` docstring, I end up writing the same boilerplate in every codebase:

```python
import rdkit.Chem.AllChem as rdkit

smiles = stk.MoleculeKeyMaker(
    key_name='SMILES',
    get_key=lambda molecule: rdkit.MolToSmiles(molecule.to_rdkit_mol()),
)
db = stk.MoleculeMongoDb(
    mongo_client=client,
    jsonizer=stk.MoleculeJsonizer(
        key_makers=(stk.InchiKey(), smiles),
    ),
)
```

A couple of problems with this DIY approach:

1. It's pure boilerplate that every user repeats. `Inchi` and `InchiKey` aren't asymmetrical — there's no reason SMILES should be the odd one out.

2. The naive `rdkit.MolToSmiles(molecule.to_rdkit_mol())` isn't a great key. For molecules built from 3D geometry (which is the normal case in stk), stereochemistry encoded in the coordinates isn't reflected in the resulting SMILES, so two molecules that should produce different keys end up with the same one. Users have to know to do extra work on the rdkit mol before calling `MolToSmiles` to get a key that's actually well-defined and consistent.

Could we get a `stk.Smiles()` key maker that mirrors `stk.Inchi()` / `stk.InchiKey()` and produces a stable, well-defined SMILES suitable for use as a database key?

Expected usage:

```python
import stk

jsonizer = stk.MoleculeJsonizer(
    key_makers=(stk.Smiles(), ),
)
json = jsonizer.to_json(stk.BuildingBlock('NCCN'))
```

…and analogously in the `key_makers` tuple passed to `MoleculeMongoDb` so SMILES can be used as a lookup key.
