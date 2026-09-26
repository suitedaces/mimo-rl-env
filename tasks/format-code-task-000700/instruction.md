### Problem Statement
I’m working with CIE Lab values and need to compare colours using the HyAB metric from Abasi 2020, but I can’t find any way to do that through `colour.difference` or `delta_E`. Could you add HyAB as one of the supported colour-difference methods so I can use it like the existing metrics?

### Expected outcomes
- `colour.difference.delta_E_HyAB(Lab_1, Lab_2)` is available for CIE L*a*b* inputs and returns the HyAB colour-difference value as defined by Abasi 2020.
- `colour.difference.delta_E(Lab_1, Lab_2, method="HyAB")` selects the same HyAB result, and HyAB is discoverable through the existing public `colour.difference.DELTA_E_METHODS` method registry.
- The `colour.difference` documentation includes a HyAB entry and lists `delta_E_HyAB` in the public API summary.

### Implementation notes
- Match the existing colour-difference API style used in this package.
- The exact internal structure, helper layout, dispatch mechanism, and validation placement are up to the implementation, as long as the public outcomes above hold.
