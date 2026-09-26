## `String.prototype.interpolate` makes `scheduling.ts` hard to unit test

I was trying to add some unit tests around `scheduling.ts` (specifically `textInterval`, since it has the most branching logic) and hit a wall.

Minimal reproduction — a jest test that just imports `textInterval` and calls it:

```ts
import { textInterval } from "../src/scheduling";

test("textInterval formats months", () => {
    expect(textInterval(35, false)).toBeTruthy();
});
```

The test blows up at runtime because `textInterval` ends up calling something like `t("MONTHS_STR_IVL").interpolate({ interval: m })`, and `interpolate` isn't defined on strings in the test environment — the call just isn't a function.

After poking around I noticed why: `interpolate` isn't a real utility, it's attached to the global `String.prototype` in `main.ts`. So the only way for the call inside `scheduling.ts` to resolve at runtime is if `main.ts` has already been imported somewhere first, which executes the prototype patch as a side effect. In a unit test that only wants to exercise `scheduling.ts`, that side effect hasn't happened, and there's no clean way to opt into it without dragging the whole plugin entry point into the test.

Two things feel off about this:

1. From a testing standpoint, a pure function like `textInterval` shouldn't transitively depend on a global side effect from `main.ts` just to format a translated string. I'd like to be able to test scheduling logic in isolation.
2. More generally, monkey-patching the global `String.prototype` to add an `interpolate` method is the kind of thing that affects every string in the process, not just translated ones. It feels like the wrong layer for this — interpolation is something the translation helper needs, not something every string in the codebase needs.

Would it be possible to rework things so that interpolation lives with the translation layer instead of on the global string type? That would let `scheduling.ts` (and anything else that uses `t(...)` with placeholders) be tested without needing `main.ts` to have run first.

Happy to help add tests for the translation helper itself once the shape of it settles.
