[Bug]: DeprecationWarning on validate_request, validate_response
### Actual Behavior

In Python [development mode](https://docs.python.org/3/library/devmode.html), the following warnings are shown for the [documented](https://openapi-core.readthedocs.io/en/latest/validation.html) usage of `validate_request`, `validate_response`:

`/home/anders/python/openapi-core/openapi_core/shortcuts.py:320: DeprecationWarning: validate_request is deprecated for unmarshalling data and it will not return any result in the future. Use unmarshal_request function instead.`

`/home/anders/python/openapi-core/openapi_core/shortcuts.py:403: DeprecationWarning: validate_response is deprecated for unmarshalling data and it will not return any result in the future. Use unmarshal_response function instead.`

### Expected Behavior

The documented usage should not raise a `DeprecationWarning`.

The warning is there to guard against deprecated uses of the return value, so either it should not be raised until the return value is used, or an explicit flag should be added that suppresses both the return value and the warning.

### Steps to Reproduce

```python
from openapi_core import Spec
from openapi_core import validate_request, validate_response
from openapi_core.testing import MockRequest, MockResponse

spec = Spec.from_dict(
    {
        "openapi": "3.0.3",
        "info": {"title": "test", "version": "0"},
        "paths": {
            "/test": {"post": {"responses": {"200": {"description": ""}}}},
        },
    },
)
request = MockRequest("http://localhost/", "post", "/test")
response = MockResponse("")
validate_request(request, spec=spec)
validate_response(request, response, spec=spec)
```

(Run with `PYTHONDEVMODE=1`.)

### OpenAPI Core Version

0.17.1

### OpenAPI Core Integration

none

### Affected Area(s)

validation

### References

_No response_

### Anything else we need to know?

_No response_

### Would you like to implement a fix?

None
