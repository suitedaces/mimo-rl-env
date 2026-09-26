# Problem Statement

I'm trying to use `Predictor.predict` with a sequence labeling model and it keeps failing with a TypeError about unexpected keyword arguments. The model follows the framework's sequence-labeling forward interface, but Predictor does not appear to be respecting the task I set when it forwards prepared inputs to the model. Can it call the network in a way that matches the task I'm doing? And if I pass some task name it doesn't know about, I'd rather get a clear error up front than a confusing crash deep inside the model.

# Expected outcomes

- Sequence labeling prediction:
  - The forwarding step used by `Predictor.predict` should work for `task="seq_label"` with a sequence-labeling model that only accepts the task-appropriate model inputs, even when the prepared batch/input contains additional fields.
  - Sequence-labeling prediction should still return the normal predicted-label output for that task rather than exposing raw intermediate model output.

- Text classification prediction:
  - The forwarding step used by `Predictor.predict` should continue to support `task="text_classify"` with the task-appropriate model input expected by text classification models.
  - Text classification prediction should not require sequence-labeling-specific post-processing behavior from the model.

- Unknown task handling:
  - If `Predictor` is used with an unsupported task name, prediction should fail early with a clear `NotImplementedError`.
  - The error message should make it clear that the task is unknown or unsupported.

# Implementation notes

- The exact dispatch structure and where validation is performed are up to the implementer.
- Keep the behavior aligned with the existing `Predictor` data preparation and batching flow.
- Avoid requiring models for one supported task to accept inputs that belong only to another task.
