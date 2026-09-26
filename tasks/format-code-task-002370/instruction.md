# Bug

When using the Field() function with an Enum, I can set an alias, but if I try to set a title or description they are ignored for default values of both (the name of the Enum subclass for the title, and 'An enumeration' for the description).

Output of `python -c "import pydantic.utils; print(pydantic.utils.version_info())"`:
```
             pydantic version: 1.6.1
            pydantic compiled: True
                 install path: /Users/joshourisman/.local/share/virtualenvs/forms-test-3oF3wXzB/lib/python3.8/site-packages/pydantic
               python version: 3.8.3 (default, Jun 30 2020, 11:16:06)  [Clang 11.0.0 (clang-1100.0.33.8)]
                     platform: macOS-10.15.5-x86_64-i386-64bit
     optional deps. installed: []

```
<!-- or if you're using pydantic prior to v1.3, manually include: OS, python version and pydantic version -->

<!-- Please read the [docs](https://pydantic-docs.helpmanual.io/) and search through issues to
confirm your bug hasn't already been reported. -->

<!-- Where possible please include a self-contained code snippet describing your bug: -->
```py
>>> from enum import Enum                          
>>> from pydantic import BaseModel, Field          
>>> class TestEnum(str, Enum): 
...     foo = 'foo' 
...     bar = 'bar'                                
>>> class TestModel(BaseModel): 
...     test: TestEnum = Field(alias='functioning_alias', title='I Will Be Ignored')                      
>>> TestModel.schema()                             
{'title': 'TestModel', 'type': 'object', 'properties': {'functioning_alias': {'$ref': '#/definitions/TestEnum'}}, 'required': ['functioning_alias'], 'definitions': {'TestEnum': {'title': 'TestEnum', 'description': 'An enumeration.', 'enum': ['foo', 'bar'], 'type': 'string'}}}
```

# Bug

Output of `python -c "import pydantic.utils; print(pydantic.utils.version_info())"`:
```
D:\Develop\pydantic>python -c "import pydantic.utils; print(pydantic.utils.version_info())"
             pydantic version: 1.6.1
            pydantic compiled: False
                 install path: D:\Develop\pydantic\pydantic
               python version: 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)]
                     platform: Windows-10-10.0.19041-SP0
     optional deps. installed: []

```
<!-- or if you're using pydantic prior to v1.3, manually include: OS, python version and pydantic version -->

<!-- Please read the [docs](https://pydantic-docs.helpmanual.io/) and search through issues to
confirm your bug hasn't already been reported. -->

<!-- Where possible please include a self-contained code snippet describing your bug: -->

```py
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Operation(Enum):
    """
    Enum that represents comparison operations.
    """
    MORE = ">"
    LESS = "<"


class Test(BaseModel):
    operation: Operation = Field(default=Operation.LESS,
                                 description="Operation used to compare something with something.")


print(Test.schema_json(indent=2))
"""
prints:

{
  "title": "Test",
  "type": "object",
  "properties": {
    "operation": {
      "$ref": "#/definitions/Operation"
    }
  },
  "definitions": {
    "Operation": {
      "title": "Operation",
      "description": "Enum that represents comparison operations.",
      "enum": [
        ">",
        "<"
      ]
    }
  }
}
"""
```
Its expected to have default value and description alongside with $ref.

Fix is pretty straightforward:
```diff
diff --git a/pydantic/schema.py b/pydantic/schema.py
index 27c66b2..ee8b331 100644
--- a/pydantic/schema.py
+++ b/pydantic/schema.py
@@ -702,6 +702,10 @@ def field_singleton_schema(  # noqa: C901 (ignore complexity)
         enum_name = normalize_name(field_type.__name__)
         f_schema = {'$ref': ref_prefix + enum_name}
         definitions[enum_name] = enum_process_schema(field_type)
+        if not schema_overrides:
+            return f_schema, definitions, nested_models
+        else:
+            return {'allOf': [f_schema]}, definitions, nested_models
     else:
         add_field_type_to_schema(field_type, f_schema)

```
