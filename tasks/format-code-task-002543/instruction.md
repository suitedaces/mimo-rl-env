## Problem Statement

Dnspython’s type information has drifted between the implementation and the adjacent stub files, and the async backend interfaces are harder to type-check than they should be because some capabilities common to the concrete backends are not represented consistently at the shared abstraction level. I’d like the package to move toward inline type information as the single source of truth while keeping the existing runtime behavior stable, except for the small public-surface fixes called out below.

## Expected outcomes

- Public package exports:
  - `from dns import *` should make the public submodules `dnssectypes` and `zonetypes` available in the importing namespace.
  - The package’s public wildcard-export metadata should be consistent with that behavior.

- Async backend shared interface:
  - Backend objects should expose the same awaitable delay capability that concrete async backends already provide, with a clear “not implemented by the base object” failure mode when used directly.
  - The shared datagram socket abstraction should treat the socket family as part of the datagram socket interface: constructing it with a family value should preserve that value on `.family`, and datagram socket instances provided by supported async backends should continue exposing the correct `.family`.

- Type-checking workflow:
  - Inline annotations should replace the relevant adjacent stub-only type information for library modules without changing the intended runtime behavior of the package.
  - The existing library type-checking make target should focus on the `dns/` package code instead of mixing in examples and tests.
  - Provide a separate make target, `potypetests`, for type-checking `examples/` and `tests/` with settings appropriate for less-completely-annotated code.

## Implementation notes

- Preserve existing public runtime APIs unless an expected outcome above explicitly calls for a surface adjustment.
- The exact organization of annotations, helper code, and internal refactoring is up to the implementation, provided the public behavior and type-checking workflow match the expected outcomes.
- Keep async backend abstractions consistent with the concrete backends’ observable behavior; tests should validate final behavior rather than a particular delegation path.
