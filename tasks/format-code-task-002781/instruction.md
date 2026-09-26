I'm using `on` from `svelte/events` in a TS project and `on(node, 'pointerdown', (e: PointerEvent) => {})` gets rejected because the handler isn't assignable to `EventListener`. I also hit a type error with `on(window.matchMedia(query), 'change', listener)` since `MediaQueryList` isn't an `Element`.

Expected outcomes:
- `on` from `svelte/events` should type-check when used with an `HTMLElement` and a known HTML event name whose listener expects that event's specific type, such as a pointer event listener for `'pointerdown'`.
- For known HTML event names on `HTMLElement` targets, listener parameters should be contextually typed according to the corresponding DOM event map rather than only as a generic `Event`.
- `on` should also type-check for non-element values that are valid `EventTarget`s, such as a `MediaQueryList`, when called with a string event name and a compatible event listener.
- Existing invalid target usage should remain rejected by TypeScript.

Implementation notes:
- The fix should preserve the public `svelte/events` API shape and runtime behavior while correcting its TypeScript-facing contract.
- The exact type declarations, overload organization, and source/type-generation plumbing are up to the implementation, as long as the observable TypeScript behavior above is satisfied.
