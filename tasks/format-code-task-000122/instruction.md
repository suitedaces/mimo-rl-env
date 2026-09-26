# Problem Statement

I'm hitting a circular import the moment I try to use anything from `idaes.core.components` on its own — importing a Component should not require the generic property package dependency chain to be pulled in first. I shouldn't have to drag in the whole generic property package just to define a component. It would be great if `idaes.core.components` could stand on its own while still supporting parameter values populated from component configuration data.

# Expected outcomes

- `idaes.core.components` can be imported and used independently without depending on the generic property-package utility path that participated in the circular import.
- A core-level public utility is available as `idaes.core.util.misc.set_param_from_config(block, parameter_name, config=None, index=None)` for setting a parameter-like Pyomo object on a block from parameter data stored on a configuration block.
- The parameter-population behavior preserves the existing user-facing semantics for scalar parameter data, unit-aware tuple data, explicit versus default configuration blocks, indexed parameter entries, and clear errors for common misuse such as missing configuration, invalid configuration objects, missing target parameters, or missing parameter-data entries.

# Implementation notes

- Keep the dependency direction such that core component definitions do not need to import generic property-model modules.
- The exact internal organization, helper boundaries, and validation placement are up to the implementer, as long as the public behavior above is preserved.
- Prefer behavior-preserving changes over broad rewrites of property models or component APIs.
