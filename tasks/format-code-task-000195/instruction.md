## Error messages from several detection ops and distribution classes are not informative

When I'm prototyping detection / probabilistic models with Paddle, I keep running into the same frustration: when I pass something wrong into these APIs, the error I get back doesn't really help me figure out what's wrong.

A few concrete cases I've hit:

**1. Shape / rank mismatch reports don't tell me what I actually passed.**

For example with `locality_aware_nms` and `mine_hard_examples`, if my `BBoxes` / `Scores` / `ClsLoss` tensors don't have the expected rank or the dimensions don't line up between two inputs, I get a message like

> "The rank of Input(Scores) must be 3"

or

> "Batch size of ClsLoss and MatchIndices must be the same."

That tells me what's expected, but not what the op actually received. If I'm debugging a pipeline where shapes are computed dynamically, I have no idea whether I sent in a rank-2 tensor, a rank-4 tensor, or whether the mismatch is 32 vs 64 or 32 vs 33. I end up `print(x.shape)`-ing every input by hand.

Same thing in `roi_perspective_transform`: messages like "The format of input tensor is NCHW." or "The transformed output height must greater than 0" don't echo back the bad value.

**2. Python-side type errors fall through to the C++ layer.**

The distribution classes `Normal`, `Uniform`, `Categorical`, `MultivariateNormalDiag` don't seem to validate their constructor / method arguments at the Python entry point. If I accidentally pass an `int` where a `float`/`ndarray`/`Variable` is expected for `loc` / `scale` / `logits`, or pass the wrong thing to `.sample(shape, seed)` / `.log_prob(value)` / `.kl_divergence(other)`, the failure happens deep inside the framework with a trace that points to internal tensor ops, not to my call site.

The Python entry points of `roi_perspective_transform` and `locality_aware_nms` have the same issue — wrong dtype on `input` / `bboxes` / `scores`, or a wrong type for one of the scalar attributes (`transformed_height`, `score_threshold`, `nms_top_k`, etc.) only blows up later.

**3. `mine_hard_examples` attribute checks are similarly opaque** — e.g. `neg_pos_ratio must greater than zero in max_negative mode` doesn't include the offending value.

### What I'd like

For these ops/classes (`Normal`, `Uniform`, `Categorical`, `MultivariateNormalDiag`, `roi_perspective_transform`, `locality_aware_nms`, `mine_hard_examples`):

- When an input has the wrong shape / rank / dimension / value, the error message should include the actual offending value so I can see at a glance what I sent in.
- Obvious type / dtype mistakes on the user-facing API should be caught right at the Python entry point with a message that names the offending argument and the API it was passed to, instead of leaking through to the C++ kernel.

This is purely a usability/diagnostics improvement — the op semantics shouldn't change for valid inputs.
