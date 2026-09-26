[SIM117] Merge with statements for context managers that have same scope
## Explanation

A little known feature of Python is that a with statement can contain multiple context managers. This allows the code only one with statement (and therefore only 1 level of indentation). This rule has a similar rational to SIM102. 

This rule should be applied if and only if:
* context A only contains the code of Context B and no other code. That is all the code in the nested statement will run with context A and B. 

Caveat when implementing: If the context names are really long, the with statement may be broken over a line break. A new feature in the Python 3.10 alpha will be to allow parentheses to be used to break the with statement over multiple lines.

## Example
Consider the following context managers:
```python
#bad
with A() as a:
    with B() as b:
        print('hello')
```
can be transformed into the following:
```python
# Good
with A() as a, B() as b:
    print('hello')
```
