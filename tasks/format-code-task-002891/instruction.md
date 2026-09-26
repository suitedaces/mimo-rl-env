## `RawFilter` requires a lot of boilerplate to instantiate

When I'm writing a custom node visitor / compiler pass that needs to wrap an
expression in a `RawFilter` (to prevent automatic escaping in the generated
template code), I currently have to write something like this every time:

```php
use Twig\Node\Expression\ConstantExpression;
use Twig\Node\Expression\Filter\RawFilter;
use Twig\Node\Node;

$wrapped = new RawFilter(
    $expression,
    new ConstantExpression('raw', $expression->getTemplateLine()),
    new Node(),
    $expression->getTemplateLine()
);
```

This is pretty awkward considering that `RawFilter::compile()` only ever
subcompiles the wrapped node — it doesn't actually look at the filter name
constant or at the arguments node at all. So every caller is forced to
construct two throw-away objects (a `ConstantExpression` and an empty `Node`)
and re-thread the line number out of the wrapped expression, just to satisfy
the parent `FilterExpression` constructor signature.

It would be nice if instantiating `RawFilter` was as simple as:

```php
$wrapped = new RawFilter($expression);
```

i.e. only the node being wrapped is mandatory, and the rest can be filled in
sensibly by `RawFilter` itself, since it doesn't use them anyway.
