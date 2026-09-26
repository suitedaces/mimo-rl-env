## macwire picks up methods with parameters as wiring candidates

I have a module class that wires a couple of services, and it also has a few
helper methods that take arguments and happen to return types that are needed
elsewhere in the wiring. When I use `wire[X]`, macwire seems to consider these
parametric helpers as valid candidates, and the macro expansion fails to
compile.

Minimal repro:

```scala
class MyDep(prefix: String)
class MyService(dep: MyDep)

class MyModule {
  // a helper that builds a MyDep with a configurable prefix
  def makeDep(prefix: String): MyDep = new MyDep(prefix)

  lazy val myService = wire[MyService]
}
```

This doesn't compile — macwire appears to treat `makeDep` as the source for
the `MyDep` argument of `MyService`, but `makeDep` needs a `String` argument
so the generated expression is invalid. The only way I can get this to work
is to either rename / move the helper out of the module, or add a separate
`val myDep: MyDep = ...` and hope the helper isn't picked instead.

I'd expect macwire to ignore methods that take parameters entirely when
collecting wiring candidates. A `def foo(x: A): B` isn't a value of type `B`
(it's a function from `A` to `B`), so it shouldn't satisfy a `B` dependency.
Only `val`s and parameterless `def`s should be considered.
