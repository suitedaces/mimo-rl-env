## prettier strips curly braces from `$obj->{...}` even when it changes the meaning

I was running prettier (with the PHP plugin) on a project that uses some dynamic property lookups, and noticed that the output was no longer equivalent to the input — running prettier with AST comparison enabled flags it.

Roughly the kind of thing I had:

```php
$obj->{foo()};
// or similar where the thing inside the braces is not a plain bareword
```

After prettier runs, the curly braces around the property name are removed. The problem is that `$obj->{foo()}` and `$obj->foo()` mean two completely different things in PHP — the first evaluates the expression inside `{...}` to get the property name, the second is a method call on `$obj` named `foo`. So removing the braces here silently changes what the program does.

It looks like the property-lookup printer is treating the curly braces as purely cosmetic and dropping them whenever the offset "looks simple enough", but it's being too aggressive: there are cases inside `->{...}` where the braces are load-bearing and removing them is not a no-op.

The plain `$obj->foo` / `$obj->$bar` cases (where the braces really are redundant) should still be unwrapped like before — only the cases where the unwrapping would actually change semantics need to keep their braces.
