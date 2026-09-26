## Problem Statement

I'm running into a weird issue with `useModel`: when I do `setState((state) => { state.count += 1 })`, the model state ends up as `undefined`, and when I do `setState({ count: 5 })` my other fields like `name` disappear. I also noticed an action middleware that calls `action()` around this setter seems to trigger my updater logic more than once. I'm hitting this while moving code from `4.0.x` to `4.1.x`, and the README doesn't really show how the old `Model`/registry/`useStore` setup maps to the new `createStore` style.

## Expected Outcomes

- `useModel` setters created inside `createStore` should support function updaters that mutate the provided state object without returning a value; the mutation should be reflected in the store and the state should not become `undefined`.
- When the current model state is an object and the setter receives an object, the update should behave like a shallow partial update: changed keys are updated and unrelated existing keys remain available.
- Action middleware that invokes the setter action should observe the completed setter result for function updaters without causing the updater callback to execute more than once for a single setter call.
- The README FAQ should include a migration guide for moving from `4.0.x` to `4.1.x`, covering the shift from the old `Model`/registry/`useStore` pattern to the `createStore`-based pattern.

## Implementation Notes

- Preserve the existing public `createStore`, `useModel`, middleware, and store usage style while adjusting the observable setter behavior.
- The exact internal state-update mechanism, validation location, and documentation wording are up to the implementation as long as the public behavior and migration guidance are clear.
