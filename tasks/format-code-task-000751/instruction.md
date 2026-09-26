### `missing-test-assertion` doesn't catch missing assertions in custom test wrappers

We use `dart-code-metrics` and recently enabled the `missing-test-assertion` rule. It works fine when we write tests directly with `test(...)` or `testWidgets(...)`, but it doesn't help us at all on the tests that go through our own helpers.

In our codebase (and I think this is pretty common in larger Flutter projects) we have a thin wrapper around `test`/`testWidgets` that sets up some shared boilerplate — something like:

```dart
void companyTest(String description, FutureOr<void> Function() body) {
  test(description, () async {
    // shared setup for our company's tests
    await body();
  });
}
```

and then test files use it like:

```dart
void main() {
  companyTest('does the thing', () {
    final a = 1;
    final b = a + 1;
    // oops, forgot the expect(...)
  });
}
```

The whole reason we wanted this rule on was to catch exactly this kind of mistake, but the linter stays silent on `companyTest` calls. From the rule docs it looks like only `test` and `testWidgets` are recognized as test methods, with no way to extend that list. `include-assertions` already lets us teach the rule about extra assertion functions (we use it for `verify` from mocktail), so it'd be very natural to have an analogous knob on the test-method side.

Could the rule be made configurable so we can tell it which additional functions should be treated as test methods? That way teams using custom wrappers, or test helpers from third-party packages, can actually benefit from the rule. The new config key would presumably be something like `include-methods`, mirroring `include-assertions`.
