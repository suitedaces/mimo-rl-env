Cannot initialize a ColumnSchema without initialized Ordinal logical type
PR #870 made a change which allowed users to initialize a column schema object with an ordinal logical type, without first instantiating the ordinal logical type, as long as the column schema was not tied to data. This seems to have been broken with the 0.4.0 release of woodwork, and it is no longer possible to do this.

The ability to use a non-instantiated Ordinal logical type is needed/preferred for the Featuretools integration.

#### Code Sample - Woodwork 0.3.1

```python
>>> from woodwork.column_schema import ColumnSchema
>>> from woodwork.logical_types import Ordinal
>>> ColumnSchema(logical_type=Ordinal)
<ColumnSchema (Logical Type = Ordinal)>

```

#### Code Sample - Woodwork 0.4.0

```python
>>> from woodwork.column_schema import ColumnSchema
>>> from woodwork.logical_types import Ordinal
>>> ColumnSchema(logical_type=Ordinal)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/nate.parsons/dev/tmp/ordinal-test/env/lib/python3.8/site-packages/woodwork/column_schema.py", line 35, in __init__
    logical_type = logical_type()
  File "/Users/nate.parsons/dev/tmp/ordinal-test/env/lib/python3.8/site-packages/woodwork/logical_types.py", line 369, in __init__
    raise TypeError("Must use an Ordinal instance with order values defined")
TypeError: Must use an Ordinal instance with order values defined

```
