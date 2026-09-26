I'm seeing `unicorn/consistent-function-scoping` report `Move function to the outer scope.` for an inner React helper that returns JSX and uses values from the surrounding component scope. It happens with both a nested function declaration and a nested arrow function returning JSX.

Expected outcomes:
- `unicorn/consistent-function-scoping` should not report inner function declarations whose body contains JSX that uses values from the surrounding scope.
- `unicorn/consistent-function-scoping` should not report nested arrow functions whose body contains JSX that uses values from the surrounding scope.
- The rule documentation should mention that functions containing JSX are ignored and include a JSX example.

Implementation notes:
- The specific analysis strategy, traversal state, and internal helper structure are up to the implementation.
- Preserve the existing behavior of `unicorn/consistent-function-scoping` for non-JSX functions.
