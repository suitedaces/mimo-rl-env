## Can't add or delete links from the store

I'm working on the patch editor and trying to wire up link creation/deletion the same way nodes already work. For nodes I can dispatch an add/delete action and the `nodes` reducer updates the store correctly — a new node gets an auto-assigned id, a delete by id removes it, and the `Patch` component re-renders.

For links there's no equivalent. Looking at `app/reducers/links.js`:

```js
export const links = (state, action) => {
  const newState = (state === undefined) ? update(state, {
    $set: initialState.project.links,
  }) : state;
  switch (action.type) {
    default:
      return newState;
  }
};
```

It only initializes from `initialState.project.links` and ignores every action. There are no link-related entries in `actionTypes.js` either, and no action creators in `actions.js`. So if I want to add a link between two pins or remove an existing one, there's currently no path to do it through redux.

Could we get add/delete support for links, mirroring how `nodes` already handles `NODE_ADD` / `NODE_DELETE` (auto id assignment on add, remove by id on delete)? Move support can come later — it probably belongs in the path reducer anyway.
