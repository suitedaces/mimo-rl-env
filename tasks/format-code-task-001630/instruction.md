toEqual throws a TypeError when using getter to private field of class
## 🐛 Bug Report

Jest throws a `TypeError` when using `toEqual` or `toMatchObject` in a class with private fields (those starting by `#`) and a getter that exposes the value. I guess other similar matchers like `toStrictEqual` also fails but didn't test. I tested this using jest-circus and fails the same way. 

The class under test has a private field `#foo` and a getter `get foo()` that returns the value of `#foo`. Using `toMatchObject` with the name of the getter (something like `.toMatchObject({ foo: 0 })`) works when the value is equal but throws a `TypeError` when are distinct (I bet when trying to show the differences, but I haven't debugged).

## To Reproduce

```js
class X {
  #foo = 42;
  get foo() {
    return this.#foo;
  }
}

test("it works and test pass", () => {
  const x = new X();
  expect(x.foo).toEqual(42);
});

test("it also works and test pass", () => {
  const x = new X();
  expect(x).toMatchObject({ foo: 42 });
});

test("it works, the test fail since values are distinct", () => {
  const x = new X();
  expect(x.foo).toEqual(0);
  // Expected: 0, Received: 42
});

test("it doesn't work, matcher throws a TypeError", () => {
  const x = new X();
  expect(x).toMatchObject({ foo: 0 });
  // TypeError: Cannot read private member #foo from an object whose class did not declare it
});

test("also doesn't work, matcher throws a TypeError", () => {
  const x = new X();
  expect(x).toEqual({ foo: 0 });
  // TypeError: Cannot read private member #foo from an object whose class did not declare it
});
```

## Expected behavior

Last two test fail properly since property `foo` are distinct between expected and received objects, showing the right report.

## envinfo

```plain
  System:
    OS: Linux 5.6 Arch Linux
    CPU: (8) x64 Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz
  Binaries:
    Node: 12.17.0 - /usr/bin/node
    npm: 6.14.5 - /usr/bin/npm
  npmPackages:
    jest: ^26.0.1 => 26.0.1 
```
