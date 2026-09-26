## Feature request: auto-set D4 damping parameters for r2SCAN in the VASP copilot

When I run r2SCAN-D4 calculations with the `Vasp` calculator, I always have to remember to set the D4 damping parameters (`VDW_S6`, `VDW_S8`, `VDW_A1`, `VDW_A2`) manually in the INCAR. These are fixed values that come from the r2SCAN-D4 parameterization — they're not something a user is supposed to tune per-system, they're just the published damping constants for that functional/dispersion combination.

Since the INCAR copilot already auto-recommends a bunch of related settings (LASPH for meta-GGAs, ALGO = All for meta-GGAs, etc.), it would be natural for it to also fill in the r2SCAN-D4 damping constants when it sees `METAGGA = r2SCAN` and the user hasn't supplied their own damping values. Right now if I forget to set them I either get whatever VASP defaults to (which is wrong for D4) or I have to copy-paste the magic numbers into every job script.

Reasonable behavior would be:

- If `METAGGA` is `r2SCAN` and none of the four damping parameters are already set by the user → copilot fills in the standard r2SCAN-D4 values and logs that it did so (consistent with the other copilot recommendations).
- If the user has explicitly set any of them → leave their choice alone, same as the rest of the copilot rules.

This would remove a class of silent-wrong-result bugs for anyone running r2SCAN-D4 with quacc.
