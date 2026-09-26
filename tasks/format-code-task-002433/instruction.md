Strict equality false positive with lists having different item types
This generate a false positive when using `--strict-equality`:
```py
class C: pass
class D:
    def __eq__(self, other): return True

a = [C()]
b = [D()]
C() == D()  # No error
print(a == b)  # error: Non-overlapping equality check (left operand type: "List[C]", right operand type: "List[D]")
```
