t.like not handling arrays as expected
I am trying to use the `t.like` assertion on deep objects with arrays of objects in them.

The following simplified example fails:
```ts
import test from 'ava';

test('deep t.like', (t) => {
  t.like({ a: [{ a: 1, b: 2 }] }, { a: [{ a: 1 }] });
});
```
```
> tsc -b

$ ava dist/ava.spec.js

  deep t.like

  Difference:

    {
      a: [
        {
          a: 1,
  -       b: 2,
        },
      ],
    }

  › src/ava.spec.ts:4:5

  ─

  1 test failed
error Command failed with exit code 1.
```

I expected the above assertion to pass. 
It seems that elements within arrays need to be deep equal rather than "like" for the assertion to pass.


AVA version:
```
$ ava --version
3.14.0
```
