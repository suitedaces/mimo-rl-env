## `ofType` doesn't work with redux-actions action creators

I'm using redux-observable together with [redux-actions](https://github.com/redux-utilities/redux-actions). Action creators produced by `createAction` override `toString()` to return their action type, which lets me skip writing string constants entirely. In a reducer this is great:

```js
const fetchUser = createAction('FETCH_USER');

const reducer = handleActions({
  [fetchUser]: (state, action) => { /* ... */ },
}, initialState);
```

I'd like the same ergonomics in my epics, but it doesn't work:

```js
const fetchUserEpic = action$ =>
  action$.ofType(fetchUser)   // never matches anything
    .switchMap(/* ... */);
```

The epic just never fires. To make it work today I have to do:

```js
action$.ofType(fetchUser.toString())
```

which defeats the whole point of using `createAction` — I'm back to manually threading the action type around, and the call site looks inconsistent with how the same creator is used in the reducer.

It would be nice if `ofType` accepted an action creator directly and matched actions of its corresponding type, while still supporting the existing string usage (`ofType('FETCH_USER')`, multiple keys, etc.) unchanged.
