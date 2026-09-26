I'm trying to use GoogLeNet from GluonCV, but `get_model('googlenet', pretrained=False)` throws a `ValueError`, and when I instantiate it directly I still hit errors during construction/forward on my current MXNet setup.

Expected outcomes:
- Model zoo lookup: `gluoncv.model_zoo.get_model('googlenet', pretrained=False)` should return a GoogLeNet model instance instead of rejecting the model name.
- Direct API usability: `gluoncv.model_zoo.googlenet.googlenet()` should be constructible with the default settings supported by the existing public API.
- Runtime usability: a default GoogLeNet model should be initializable and should accept normal image batch tensors for forward passes on the current supported MXNet/Gluon runtime.
- Public model surface: the existing public GoogLeNet entry points, including `gluoncv.model_zoo.googlenet` and `gluoncv.model_zoo.GoogLeNet`, should remain usable.

Implementation notes:
- Keep the fix behavior-focused: the exact internal layer organization, helper functions, naming, and compatibility mechanism are up to the implementation.
- Preserve the existing public API shape for callers unless a behavior above requires exposing an already-public entry point through the model zoo.
- Do not require pretrained weights for the non-pretrained lookup or forward-pass path.
