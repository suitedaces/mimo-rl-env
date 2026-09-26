Literal field and tagged union
The following simple example, which uses a [`Literal`](https://www.python.org/dev/peps/pep-0586/), doesn't work (because `marshmallow-dataclass` doesn't seem to support `Literal`):

```python
from dataclasses import dataclass

from marshmallow_dataclass import class_schema
from typing_extensions import Literal

@dataclass
class A:
    choices: Literal['x', 'y']

Schema = class_schema(A)  # ERROR
```

This is the error:

```
.../site-packages/marshmallow_dataclass/__init__.py:316: UserWarning: marshmallow_dataclass was called on the class typing_extensions.Literal['x', 'y'], which is not a dataclass. It is going to try and convert the class into a dataclass, which may have undesirable side effects. To avoid this message, make sure all your classes and all the classes of their fields are either explicitly supported by marshmallow_datcalass, or are already dataclasses. For more information, see https://github.com/lovasoa/marshmallow_dataclass/issues/51
  f"marshmallow_dataclass was called on the class {clazz}, which is not a dataclass. "
Traceback (most recent call last):
  File ".../site-packages/dataclasses.py", line 970, in fields
    fields = getattr(class_or_instance, _FIELDS)
AttributeError: '_Literal' object has no attribute '__dataclass_fields__'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 312, in _internal_class_schema
    fields: Tuple[dataclasses.Field, ...] = dataclasses.fields(clazz)
  File ".../site-packages/dataclasses.py", line 972, in fields
    raise TypeError('must be called with a dataclass type or instance')
TypeError: must be called with a dataclass type or instance

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 323, in _internal_class_schema
    created_dataclass: type = dataclasses.dataclass(clazz)
  File ".../site-packages/dataclasses.py", line 958, in dataclass
    return wrap(_cls)
  File ".../site-packages/dataclasses.py", line 950, in wrap
    return _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)
  File ".../site-packages/dataclasses.py", line 764, in _process_class
    unsafe_hash, frozen))
AttributeError: '_Literal' object has no attribute '__dataclass_params__'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 303, in class_schema
    return _internal_class_schema(clazz, base_schema)
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 344, in _internal_class_schema
    for field in fields
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 345, in <genexpr>
    if field.init
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 526, in field_for_schema
    nested_schema or forward_reference or _internal_class_schema(typ, base_schema)
  File ".../site-packages/marshmallow_dataclass/__init__.py", line 327, in _internal_class_schema
    f"{getattr(clazz, '__name__', repr(clazz))} is not a dataclass and cannot be turned into one."
TypeError: typing_extensions.Literal['x', 'y'] is not a dataclass and cannot be turned into one.
```

I think `Literal` is quite useful, e.g. for creating tagged unions. Is there any chance to add support for `Literal` to `marshmallow-dataclass`?
