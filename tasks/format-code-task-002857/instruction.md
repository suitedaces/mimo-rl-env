Support MySQL unsigned integer
MySQL supports unsigned integer data type.
This can occur in two forms, with a parameterized int and without. 
```python
import sqlglot

sql = "CREATE TABLE t (id INT UNSIGNED)"
sql_parameterized = "CREATE TABLE t (id INT(10) UNSIGNED)"
sqlglot.parse_one(sql, read="mysql")
sqlglot
```
Now there is an exception in the library when parsing such a syntax.
Related discussion #2164 

**Official Documentation**
https://dev.mysql.com/doc/refman/8.0/en/numeric-type-syntax.html
