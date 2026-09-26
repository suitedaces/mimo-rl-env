## Feature request: expose "am I in the first evaluation?" and "how many dependencies does this computed have?" from inside a `ko.computed`

I'm writing a custom two-way binding handler. Inside `init` I set up a `ko.computed` that reads an observable from the view model and writes the current DOM state back into it — basically the same shape as the built-in `checked` / `value` bindings. The problem is the very first evaluation: at setup time my element doesn't yet reflect the model, so if I write back unconditionally I clobber the model with whatever the element started as. I only want the "write back to model" branch to run from the *second* evaluation onward, i.e. when an actual dependency changed.

Today the only way I can do this is the usual closure-flag dance:

```js
ko.bindingHandlers.myBinding = {
    init: function (element, valueAccessor) {
        var isFirstRun = true;
        ko.computed(function () {
            var modelValue = ko.utils.unwrapObservable(valueAccessor());
            // ... read element, etc ...
            if (isFirstRun) {
                isFirstRun = false;
                return;
            }
            // write back to model
        }, null, { disposeWhenNodeIsRemoved: element });
    }
};
```

This works but it's ugly, and when I have *two* such computeds in the same handler (one syncing model → DOM, another syncing DOM → model) coordinating the flags gets fiddly — they each need their own, and you have to be careful about evaluation order. It feels like the framework already knows whether the evaluator is being run for the first time; I'd just like to be able to ask.

A related case: I'm also playing with a control-flow style binding (similar in spirit to `if`). On first evaluation I want to snapshot the inner DOM so I can restore it later when the predicate flips back to true. But if the binding's expression is a literal (no observables) then the computed has no dependencies, it'll never re-evaluate, and snapshotting is just wasted work + retained DOM nodes. I'd like to be able to check from inside the evaluator whether this computed actually has any dependencies registered, and skip the snapshot when it doesn't.

Both of these are things the computed machinery clearly already tracks internally (there's a `getDependenciesCount` on the computed instance, and the first-run vs. subsequent-run distinction obviously exists). It would be great to be able to query them from *inside* the currently-running evaluator function, without having to grab a reference to the outer `ko.computed` or maintain closure state.

Could KO expose a small public API for "the currently executing computed evaluation"? Concretely:

- a way to ask "is this the initial evaluation of the current computed?"
- a way to ask "how many dependencies has the current computed registered so far / in total?"

Both should only be meaningful when called synchronously from inside a `ko.computed` evaluator. I'd expect this to hang off something like a `ko.computedContext` namespace, with methods named along the lines of `isInitial()` and `getDependenciesCount()` — but the exact placement is up to whatever fits KO's existing API surface best.
