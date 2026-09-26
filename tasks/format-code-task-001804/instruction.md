Remove initialize() Method from LlamaStackAsLibrary
### 🚀 Describe the new functionality needed

## Summary

Remove the explicit `initialize()` method requirement from `LlamaStackAsLibraryClient` to improve developer experience and reduce the potential for initialization errors.

## Problem Statement

Currently, `LlamaStackAsLibraryClient` requires a two-step initialization process:

```python
from llama_stack import LlamaStackAsLibraryClient

client = LlamaStackAsLibraryClient("nvidia")
client.initialize()  # Required manual step - this should not be necessary
response = client.models.list()
```

This pattern creates several issues:

1. **Poor Developer Experience**: Users must remember to call an additional method after construction
2. **Error-Prone**: Easy to forget the `initialize()` call, leading to runtime errors
3. **Inconsistent with Python Best Practices**: Most Python libraries handle initialization in `__init__`
4. **Breaks Intuitive API Design**: Users expect objects to be ready for use after construction

## Desired Behavior

The client should be immediately usable after construction:

```python
from llama_stack import LlamaStackAsLibraryClient

client = LlamaStackAsLibraryClient("nvidia")  # Fully initialized
response = client.models.list()  # Works immediately
```

## Success Criteria

1. Client can be used immediately after construction without calling `initialize()`
2. No breaking changes to existing API surface (beyond removing `initialize()`)
3. Clear error messages for initialization failures
4. Backward compatibility during deprecation period
5. All existing functionality works unchanged
6. Performance impact is acceptable


### 💡 Why is this needed? What if we don't build it?

see above

### Other thoughts

_No response_
