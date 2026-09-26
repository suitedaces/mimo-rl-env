## Convenient access to the variance gradient at a single point in kriging surrogates

I'm using `KRG` (and the MFK variants) for some Bayesian-optimization-flavoured work where, at a candidate point `x*`, I need the gradient of the predicted variance — i.e. the partial derivatives of the variance with respect to *all* input dimensions, evaluated at that one point.

Looking at the public API of `SurrogateModel` / kriging-based models, the only thing I can find for variance derivatives is `predict_variance_derivatives(x, kx)`, which gives the derivative with respect to a single input component `kx`. So if my problem has `nx` inputs and I want the gradient at a point, I end up doing something like:

```python
grad = np.array([
    sm.predict_variance_derivatives(x_star, kx).ravel()
    for kx in range(x_star.shape[1])
])
```

This works but feels off:

* It's `nx` separate predict calls for what is conceptually one quantity at one point.
* Every caller that wants "variance gradient at a point" has to re-implement the same loop + stacking + shape massaging, and it's easy to get the orientation of the resulting array wrong.
* For acquisition functions / optimizers that ask the surrogate for a gradient at the current iterate, this is the natural thing to want directly from the model.

It would be great if kriging-based surrogates exposed a first-class way to ask, in one call, for the gradient of the variance at a given point — taking an `x` of shape `(1, nx)` (and ideally accepting a plain `(nx,)` vector for convenience) and returning the full vector of partials at that point.

For context, `predict_variance_derivatives(x, kx)` already covers the "set of points, one component" case and should keep working as it does today; what's missing is the dual "one point, all components" case. The two together would cover the typical use cases nicely.

A natural name for the new entry point would be something like `predict_variance_gradient(x)`.
