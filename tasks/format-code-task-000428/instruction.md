# Add a runtime factory for optimizers

SINGA's C++ model library provides several gradient-descent optimizers (vanilla
SGD with momentum, Nesterov, Adagrad and RMSProp). Today the only way to obtain
one is to name the concrete class at compile time. Code that drives training
from a configuration or from a binding layer needs to pick the optimizer at
runtime from a plain type name, so we want a small factory in the optimizer
public API.

Add a function

```cpp
std::shared_ptr<singa::Optimizer> singa::CreateOptimizer(const std::string& type);
```

that constructs the optimizer selected by `type` and returns it through the
common `Optimizer` base class, so the caller can drive it polymorphically
(`Setup`, `Apply`, etc.) without knowing the concrete type. It must be reachable
from the optimizer's public header, i.e. any translation unit that includes the
optimizer header can call it.

Requirements:

- The accepted type names are exactly `"SGD"`, `"Nesterov"`, `"Adagrad"` and
  `"RMSProp"`. Each must yield an optimizer that performs that algorithm's
  update: an object created with a given name, once set up and applied, must
  produce the same parameter update as constructing that optimizer class
  directly and applying it the same way.
- The returned handle must be usable purely through the `Optimizer` base
  interface.
- Passing any other (unrecognized) string must fail fast — abort with a fatal
  error rather than returning a null or otherwise unusable optimizer.

No change to the optimizers' update math is expected; this is about being able
to obtain them by name.
