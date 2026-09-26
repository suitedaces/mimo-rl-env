`Dataset.npred_signal()` should take model name
`Dataset.npred_signal()` takes a model as argument, whereas in most other places (eg:`FluxPointEstimator` we access models by their names. This create some confusion.

@adonath shall I put in a PR to change this?
