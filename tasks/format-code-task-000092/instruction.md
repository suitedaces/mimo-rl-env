Allow multiple variable-rank dimension specs in check_shapes
# Feature request

Allow multiple variable-rank dimension specs in check_shapes.

## Motivation

Today we have:

```python
@check_shapes(
    "a: [a_shape...]",
    "b: [b_shape...]",
    "return: [a_shape_b_shape...]",
)
def broadcasting_elementwise(
    op: Callable[[tf.Tensor, tf.Tensor], tf.Tensor], a: tf.Tensor, b: tf.Tensor
) -> tf.Tensor:
    """ Apply binary operation `op` to every pair in tensors `a` and `b`. """
```

it would be nice to have

```python
@check_shapes(
    "a: [a_shape...]",
    "b: [b_shape...]",
    "return: [a_shape..., b_shape...]",
)
def broadcasting_elementwise(
    op: Callable[[tf.Tensor, tf.Tensor], tf.Tensor], a: tf.Tensor, b: tf.Tensor
) -> tf.Tensor:
    """ Apply binary operation `op` to every pair in tensors `a` and `b`. """
```

This is hard for reasons similar to why GPflow/check_shapes#5 is hard. In general, if there are multiple variable-rank dimensions in one specification, we cannot determine which dimensions belong to which variable. We could solve this is a couple of ways:

1. Require the user to specify their checks in an order, so that there always is at most one variable-rank dimension with **unknown** size, at the time the constraint is evaluated.
2. Evaluate constraints lazily, and on a best-effort basis. If we're trying to evaluate a constraint where we don't have enough information we simply store it for later, and hope that the necessary information becomes available.

I don't like (1), because I don't like have to impose an ordering on constraints, and because optional arguments and broadcasting can make it hard to predict when a variable value will actually be available. I like (2) better, but it does have the disadvantage that sometimes a shape variable value may never be known, and no check actually performed.
