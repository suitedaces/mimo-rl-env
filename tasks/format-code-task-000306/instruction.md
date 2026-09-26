# Make the Keras wrappers behave like real scikit-learn estimators

The `KerasClassifier` and `KerasRegressor` wrappers in this package are supposed to let a
compiled Keras model be used anywhere a scikit-learn estimator is expected, but right now they
don't actually work — they lean on Keras methods that no longer exist and they don't follow
scikit-learn's estimator conventions. Please bring them up to a fully working, scikit-learn
compatible state.

Both estimators are constructed with a `build_fn` plus any number of extra keyword arguments,
e.g. `KerasClassifier(build_fn=my_build_fn, hidden_dim=10)`. `build_fn` is a callable that
returns a **compiled** Keras model. The following three ways of supplying it must all work:

1. a plain function,
2. an instance of a class that implements `__call__`,
3. `None`, in which case the wrapper is being subclassed and the subclass itself implements
   `__call__`.

The extra keyword arguments are model/fit parameters; any of them whose names match an argument
of `build_fn` are forwarded to it when the model is built.

## scikit-learn parameter API

* `get_params()` returns a dict containing `build_fn` together with every extra keyword argument
  passed to the constructor, mapped to its current value. It accepts the usual optional `deep`
  argument.
* `set_params(**params)` updates the given parameters in place and returns the estimator itself;
  a subsequent `get_params()` reflects the new values.
* `sklearn.base.clone(estimator)` must succeed and return a new, **unfitted** estimator that
  carries the same constructor parameters.

## KerasClassifier

* `fit(X, y)` builds and trains the model and returns the estimator itself. Extra keyword
  arguments (e.g. `epochs`, `batch_size`) are forwarded to the underlying Keras `fit`. After
  fitting, `classes_` holds the sorted unique labels seen in `y` and `n_classes_` holds their
  count. The original label values must be preserved even when they are not a contiguous
  `0..k-1` range.
* `predict(X)` returns a 1-D array of shape `(n_samples,)` whose entries are drawn from
  `classes_` (i.e. the original label values, not internal indices).
* `predict_proba(X)` returns an array of shape `(n_samples, n_classes_)` whose rows sum to 1.
  For a binary problem whose network has a single output unit it must still return two columns.
* `score(X, y)` returns the mean classification accuracy as a float in `[0, 1]`.

## KerasRegressor

* `fit(X, y)` builds and trains the model and returns the estimator itself, forwarding extra
  keyword arguments to the underlying Keras `fit`.
* `predict(X)` returns a 1-D array of shape `(n_samples,)` for a single-output model.
* `score(X, y)` returns the coefficient of determination R² (as scikit-learn defines it).

## Serialization

A fitted estimator must survive a `pickle` round-trip: after unpickling it produces the same
predictions as the original.
