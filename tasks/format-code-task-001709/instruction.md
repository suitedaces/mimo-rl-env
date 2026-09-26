Root models not collapsed when using field-constraints & collapse-root-models
**Describe the bug**
Generated pydantic models have un-collapsed root models when using `--field-constraints` in combination with `--collapse-root-models`.

See the generated model:
```python

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Number(BaseModel):
    __root__: str = Field(
        ...,
        description='Just a number',
        examples=['1', '5464446', '684572369854259'],
        regex='^\\d{1,15}$',
    )


class TestSchema(BaseModel):
    numbers: List[Number] = Field(..., description='A list of numbers')

```

**To Reproduce**
Please save the json schema as `schema.json` and run the command to generate the model to reproduce.

Example schema:
```json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "TestSchema",
  "description": "For the test",
  "properties": {
    "numbers": {
      "type": "array",
      "description": "A list of numbers",
      "items": {
        "type": "string",
        "pattern": "^\\d{1,15}$",
        "description": "Just a number",
        "examples": ["1", "5464446", "684572369854259"]
      }
    }
  },
  "required": [
    "numbers"
  ]
}


```

Used commandline:
```
$ datamodel-codegen \
--input-file-type jsonschema \
--target-python-version 3.9 \
--field-constraints \
--collapse-root-models \
--input schema.json \
--output schema.py
```

**Expected behavior**
I'm expecting a generated model without the sub-model that looks more like this:
```python

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class TestSchema(BaseModel):
    numbers: List[str] = Field(
        ..., description='A list of numbers',
        regex=r'^\d{1,15}$'
    )

```

**Version:**
- OS: Ubuntu 20.04.1
- Python version: 3.9.10
- datamodel-code-generator version: 0.19.0

**Additional context**
When not using `--field-constraints` the behavior is similar to my expectations:
```python

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, constr


class TestSchema(BaseModel):
    numbers: List[constr(regex=r'^\d{1,15}$')] = Field(
        ..., description='A list of numbers'
    )
```
