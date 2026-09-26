# Fix double-backprop through shared feature networks

In our actor-critic setup, a single `FeatureNetwork` produces a feature
representation that is shared by several downstream heads (e.g. a value
function and a policy). Each head computes its own loss and calls
`.backward()`. Today, because the features the network hands out are still
wired into the feature model's computation graph, every head's backward pass
runs all the way back through the shared feature model. With two heads that
means we backpropagate through the shared model twice per update even though we
only take one optimizer step — wasteful, and it forces callers to juggle
`retain_graph=True` to avoid "backward through the graph a second time" errors.

Rework `FeatureNetwork` so the shared model is only backpropagated through
once per training step, while keeping its existing public surface
(`__call__`, `eval`, `reinforce`).

Required observable behavior:

- Calling the network on a state returns a `State` whose mask and info are
  carried over from the input, and whose feature tensor holds the model's
  output for that state. That feature tensor must be a gradient-tracking leaf
  that is **disconnected** from the feature model's graph: any number of
  downstream computations may derive a loss from it and call `.backward()`
  independently, in sequence, without passing `retain_graph` and without
  raising. The gradient each head produces accumulates on this returned
  feature tensor.

- `reinforce()` takes no loss of its own — the training signal is exactly the
  gradient that downstream heads have accumulated on the feature tensors handed
  out since the last `reinforce()`. It pushes that accumulated gradient back
  through the shared model in a single backward pass, honoring the optional
  gradient clipping, then performs one optimizer step and clears the gradients.

- The network may be called multiple times before a single `reinforce()`; all
  of those forward passes contribute their accumulated gradients to that one
  optimizer step. After `reinforce()` returns, the pending state is cleared:
  the next forward/reinforce cycle is independent and must not re-apply
  gradients from a previous cycle.

- `eval(state)` returns a `State` (mask/info preserved) whose features are the
  model output computed without building a graph (no gradient tracking), and
  it must not disturb the model's training mode.

The net effect: for a set of downstream losses, the optimizer step applied to
the shared model is exactly the single SGD-equivalent step you would get by
backpropagating the summed downstream gradient through the model once.
