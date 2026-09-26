Wrong maximum value for integer in output model
**Describe the bug**
Maximum value in the output model is wrong.
**To Reproduce**

Example schema:
```
definitions:
  testInt64:
    type: integer
    minimum: 2097152
    maximum: 9223372036854775807
```

Used commandline:
```
$ datamodel-codegen --input test-schema.yaml --output test_model.py --target-python-version 3.8
```

**Expected behavior**
Expected the output model to be:

```
class TestInt64(BaseModel):
    __root__: conint(ge=2097152, le=9223372036854775807)
```

but it is:
```
class TestInt64(BaseModel):
    __root__: conint(ge=2097152, le=9223372036854775808)
```

**Version:**
 - OS: Ubuntu 20.0.4
 - Python version: 3.8
 - datamodel-code-generator version: 0.17.1
