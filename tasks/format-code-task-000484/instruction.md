## PI and LogEI acquisition functions crash when called

I'm using RoBO for some Bayesian optimization experiments. The default `EI`
acquisition function works fine, so I wanted to compare against `PI` and
`LogEI` on the same problem.

I set them up the same way I set up `EI` (same model, same `X_lower` /
`X_upper`, same `compute_incumbent` for `LogEI`). The moment I evaluate
either of them on a candidate point, it blows up somewhere inside the call —
it never gets to return an acquisition value.

Rough sketch of what I'm doing:

```python
# this works fine
ei  = EI(model, X_lower, X_upper, compute_incumbent)
val = ei(X_test)

# this dies
pi    = PI(model, X_lower, X_upper)
val_p = pi(X_test, incumbent)

# this also dies
logei = LogEI(model, X_lower, X_upper, compute_incumbent)
val_l = logei(X_test)
```

Since `EI` works on exactly the same model/bounds, I'd expect `PI` and
`LogEI` to be usable as drop-in alternatives. Right now they aren't — only
`EI` is actually callable.

Could `PI` and `LogEI` be fixed so they also return a value the way `EI`
does?
