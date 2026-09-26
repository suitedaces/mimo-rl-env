Queue reports full with no items
A persistent queue reports full if there are no items.  This only seems to effect queues where `maxsize` is not provided or set to `0`.

When `maxsize` is zero (default), the `full()` is reported as True with no items (incorrect).
```python
>>> q = persistqueue.Queue('/tmp/mypq')
>>> q.qsize(), q.empty(), q.full()
(0, True, True)

>>> q.put('foo')
>>> q.qsize(), q.empty(), q.full()
(1, False, False)

>>> q.put('bar')
>>> q.qsize(), q.empty(), q.full()
(2, False, False)

>>> q.get(block=False)
'foo'
>>> q.qsize(), q.empty(), q.full()
(1, False, False)

>>> q.get(block=False)
'bar'
>>> q.qsize(), q.empty(), q.full()
(0, True, True)

>>> q.get(block=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/xxx/venv_3/lib/python3.7/site-packages/persistqueue/queue.py", line 178, in get
    raise Empty
persistqueue.exceptions.Empty
```

When `maxsize` is given, the `full()` is reported as False with no items (correct).
```python
>>> q3 = persistqueue.Queue('/tmp/mypq3', maxsize=2)
>>> q3.qsize(), q3.empty(), q3.full()
(0, True, False)

>>> q3.put('foo')
>>> q3.qsize(), q3.empty(), q3.full()
(1, False, False)

>>> q3.put('bar')
>>> q3.qsize(), q3.empty(), q3.full()
(2, False, True)

>>> q3.get(block=False)
'foo'
>>> q3.qsize(), q3.empty(), q3.full()
(1, False, False)

>>> q3.get(block=False)
'bar'
>>> q3.qsize(), q3.empty(), q3.full()
(0, True, False)

>>> q3.get(block=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/xxx/venv_3/lib/python3.7/site-packages/persistqueue/queue.py", line 178, in get
    raise Empty
persistqueue.exceptions.Empty
```
