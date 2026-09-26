Fine-grained error locations in Python tracebacks
With the [acceptance](https://mail.python.org/archives/list/python-committers@python.org/thread/3WDJNOW2SPTPCKUGLG2ANBWZZEYTT6F6/) of [PEP 657](https://www.python.org/dev/peps/pep-0657/), "Include fine-grained error locations in tracebacks", a Python traceback will look like this:

```
Traceback (most recent call last):
  File "test.py", line 2, in <module>
    x['a']['b']['c']['d'] = 1
    ^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not subscriptable
```

The `PythonTracebackLexer` will need some adjustments. Currently, it highlights the carets are operators (thinking it is reading Python code).
