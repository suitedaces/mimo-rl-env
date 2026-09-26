## Problem Statement

I'm building a graph where one op produces a function, and right now I have to use an awkward wrapper just to apply it to other graph values. Could you make function-valued Operations usable like normal callables from the public pythonflow API, so the actual function gets called when the graph runs? Also, when I pass a bad fetch or a non-dict context, the error is pretty confusing, so it'd be great if pythonflow failed early with a clear ValueError. It would help if the lazy import utility were exposed at the top level too, and if the dev/Docker/CI installs used the same dev requirements file.

## Expected Outcomes

- Callable operation values: an Operation whose evaluated value is callable can be called with positional and keyword graph values, producing a new operation that invokes the evaluated callable when the graph runs.
- Public call helper: `pythonflow.call(func, *args, **kwargs)` is available and produces an operation that evaluates `func` and its arguments before applying the callable.
- Invalid fetch validation: graph execution rejects invalid fetch specifications early with a clear `ValueError` instead of failing later with an indirect error.
- Invalid context validation: graph execution rejects non-mapping contexts early with a clear `ValueError`.
- Public lazy import helper: `pythonflow.lazy_import(module)` is available from the package namespace and imports the named module on first attribute access.
- Shared development dependencies: the documented development, Docker, and CI install paths use `dev-requirements.txt` as the shared dependency file.

## Implementation Notes

- Preserve the existing public graph-building and graph-execution model; the exact internal representation of the new callable operation is up to the implementation.
- Keep validation behavior focused on externally supplied fetch and context inputs, while preserving existing valid input forms.
- Expose only the public API and configuration behavior described above; helper organization, private names, and dependency-file maintenance details are implementation choices.
