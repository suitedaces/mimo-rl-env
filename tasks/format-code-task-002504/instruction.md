when the new JsonModel class fields with Literal type the class initialization throws error

```
from redis_om import (EmbeddedJsonModel, Field, JsonModel)
from typing import Optional, List, Literal


class worker(JsonModel):
    nodeName: str   = Field(index=True, description='Name of the worker node')

    Role: Literal['Part-Timer', 'Full-Timer'] = Field(index=True, default='Full-Timer')

    desiredState: Literal['Active', 'Hold', 'Error'] = Field(index=True, default='Active')

```

Trace:- 
```
.\venv\Lib\site-packages\pydantic\_internal\_config.py:341: UserWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
  warnings.warn(message, UserWarning)
Traceback (most recent call last):
  File "workerConfigModel.py", line 6, in <module>
    class worker(JsonModel):
  File ".\venv\Lib\site-packages\redis_om\model\model.py", line 1298, in __new__
    new_class = super().__new__(cls, name, bases, attrs, **kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".\venv\Lib\site-packages\pydantic\_internal\_model_construction.py", line 118, in __new__
    cls: type[BaseModel] = super().__new__(mcs, cls_name, bases, namespace, **kwargs)  # type: ignore
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen abc>", line 106, in __new__
  File ".\venv\Lib\site-packages\redis_om\model\model.py", line 1875, in __init_subclass__
    cls.redisearch_schema()
  File ".\venv\Lib\site-packages\redis_om\model\model.py", line 1944, in redisearch_schema
    schema_parts = [schema_prefix] + cls.schema_for_fields()
                                     ^^^^^^^^^^^^^^^^^^^^^^^
  File ".\venv\Lib\site-packages\redis_om\model\model.py", line 1989, in schema_for_fields
    cls.schema_for_type(json_path, name, "", _type, field_info)
  File ".\venv\Lib\site-packages\redis_om\model\model.py", line 2126, in schema_for_type
    typ = type_args[0].__origin__
          ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute '__origin__'
```
using python 3.11.4 with below package versions

annotated-types   0.7.0
cffi              1.16.0
click             8.1.7
colorama          0.4.6
cryptography      42.0.8
hiredis           2.3.2
more-itertools    10.3.0
pip               23.2.1
pycparser         2.22
pydantic          2.8.2
pydantic_core     2.20.1
python-ulid       1.1.0
redis             5.0.7
redis-om          0.3.1
setuptools        68.2.0
types-cffi        1.16.0.20240331
types-pyOpenSSL   24.1.0.20240425
types-redis       4.6.0.20240425
types-setuptools  70.3.0.20240710
typing_extensions 4.12.2
wheel             0.41.2
```
