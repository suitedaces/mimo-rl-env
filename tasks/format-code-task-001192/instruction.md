### Missing type definition for `Observable.combineAll` in rxjs v5 libdef

The flow-typed definitions for `rxjs` v5 (`definitions/npm/rxjs_v5.0.x/...`) don't seem to include the `combineAll` operator. It's a standard rxjs 5 operator (see http://reactivex.io/rxjs/class/es6/Observable.js~Observable.html#instance-method-combineAll) and works fine at runtime, but Flow complains it's not on `Observable`.

Repro — something like:

```js
import { Observable } from 'rxjs';

const higherOrder: Observable<Observable<number>> = Observable.of(
  Observable.of(1, 2, 3),
  Observable.of(4, 5, 6),
);

const combined = higherOrder.combineAll();
combined.subscribe(arr => console.log(arr));
```

Flow errors out on `.combineAll()` because the method isn't declared on `rxjs$Observable`. Other "join" operators on higher-order observables like `concatAll` and `mergeAll` are already in the libdef, so it'd be nice to have `combineAll` covered as well (in both the `flow_v0.25.0-v0.33.x` and `flow_v0.34.x-` variants).

It should also support the optional projection function form (`combineAll(project)`) that rxjs allows.
