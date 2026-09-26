## Migrate the upload plugin reducers away from `immutable.js`

The upload plugin (`packages/core/upload`) still relies on `immutable.js` for its reducer state — `fromJS`, `state.get(...)`, `state.updateIn(...)`, `state.toJS()` calls everywhere in the reducers under `admin/src`. The rest of the admin codebase has already moved to plain JS objects + `immer` for reducers, so the upload plugin is the odd one out.

### Why

- `immutable` is a fairly heavy dep and we're already shipping `immer` anyway, so keeping both inflates the build for no reason.
- It's a contribution friction point: anyone touching an upload reducer has to learn / remember the `immutable` API (`getIn`, `updateIn`, `keySeq`, `.toJS()` on the consumer side, etc.) when every other reducer in the project just mutates a draft.
- The `.toJS()` calls in components (`reducerState.toJS()`) are easy to forget and easy to misuse.

### What I'd like

Drop `immutable` from the upload plugin entirely:

- Reducers should operate on plain JS state, in the same style as the other plugins.
- Components consuming these reducers shouldn't need to call `.toJS()` on the state anymore — they should be able to destructure directly from `useReducer`.
- `init` functions for these reducers should also work with plain objects.
- Remove `immutable` from the upload plugin's `package.json` once it's no longer referenced.

Behaviorally nothing should change for end users of the Media Library — this is purely an internal refactor.
