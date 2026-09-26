Types not enforced on tuple return - bug
Attempting to compile:
```python
@public
def getTime() -> uint256:
    return block.timestamp
```
rightfully returns the error 
```
vyper.exceptions.TypeMismatchException: line 3: 
Return type units mismatch uint256(sec, positional) uint256
```

However, this compiles just fine:
```python
@public
def getTimeAndBalance() -> (bool, address):
    return block.timestamp, self.balance
```
