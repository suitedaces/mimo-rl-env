## `annotationlib.ForwardRef` 在 Python 3.14 上有几个让人意外的行为

我在用 3.14 新的 `annotationlib` 写一些 annotation 内省工具，遇到两个 `ForwardRef` 的行为，跟我从方法签名上的预期不一致。

### 1. `evaluate()` 看起来会忽略后续传进来的参数

`ForwardRef.evaluate()` 的签名接受 `globals` / `locals` / `owner` / `type_params`，所以我以为每次调用都会按这次传进来的 scope 去解析。但实际上，只要第一次成功 evaluate 过，之后再调，不管我传什么 scope 都会得到第一次的结果：

```python
>>> from annotationlib import ForwardRef
>>> ref = ForwardRef("X")
>>> ref.evaluate(globals={"X": int})
<class 'int'>
>>> ref.evaluate(globals={"X": str})
<class 'int'>
```

我期望第二次调用拿到的是 `str`，因为我明明传了不同的 globals。如果方法本来就不打算每次重新算，那 `globals`/`locals`/`owner` 这些参数在第一次之后就完全没用，这跟接口本身的形状不太一致。

### 2. scope 不同的两个 `ForwardRef` 会被当作相等

我有时会针对同一个名字、不同的 `owner` 构造多个 `ForwardRef`，因为它们其实可能解析到不同的东西（比如挂在不同 class 上的 `X`）。但这些对象在 `==` 和放进 set/dict 时会互相吃掉：

```python
>>> from annotationlib import ForwardRef
>>> class A: pass
>>> class B: pass
>>> r1 = ForwardRef("X", owner=A)
>>> r2 = ForwardRef("X", owner=B)
>>> r1 == r2
True
>>> len({r1, r2})
1
```

这两个 ref 来自不同的 owner，语义上不该是同一个引用，但相等性把它们合并了。我希望两个 `ForwardRef` 只在它们真正描述同一个引用（包括 scope 信息）时才相等，对应的 hash 行为也跟着一致。

如果能修一下就好了 —— `evaluate()` 应该每次都用当前传进去的参数解析，而不是一旦成功就锁定结果；同时 `ForwardRef` 的相等性/哈希也应该把 scope 相关的信息算进去，让 scope 不同的 ref 不互相覆盖。
