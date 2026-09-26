## No way to observe internal redux actions through SagaTester

I'm using `SagaTester` to test a saga that reacts to `@@redux/INIT` (the saga does some setup the first time the store comes up). In my test I want to assert that the action was seen and the saga reacted to it, but none of the inspection APIs ever acknowledge these internal actions:

```js
const tester = new SagaTester({ reducers });
tester.start(mySaga);

tester.getActionsCalled();          // no @@redux/* entries at all
tester.wasCalled('@@redux/INIT');   // false
await tester.waitFor('@@redux/INIT'); // never resolves
```

These actions are definitely being dispatched — the store initializes correctly and my reducers receive them — they just don't show up anywhere in the tester's tracking.

For the vast majority of tests this is the right default (nobody wants their assertions polluted by redux's internal bookkeeping actions), so I don't want to change the out-of-the-box behavior. But for the case where I *do* want to verify a saga's interaction with these internal actions, there's currently no way to do it.

Could `SagaTester` provide an opt-in for including the `@@redux/*` actions in the tracked set, while keeping today's behavior as the default so existing tests are unaffected? I'd expect the new option on the constructor to be something like `ignoreReduxActions` (defaulting to the current behavior).
