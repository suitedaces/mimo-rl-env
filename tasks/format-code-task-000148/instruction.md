Wrong error in Metric.__iter__
## 🐛 Bug
In the class `Metric`, the `__iter__` method is defined as follows:
```python
def __iter__(self):
    """Iteration over metrics are not allowed. Use metric collections for nesting metrics."""
    raise NotImplementedError("Metrics does not support iteration.")
```
In python's docs, the following note is written about `NotImplementedError` (https://docs.python.org/3/library/exceptions.html#NotImplementedError): 
> It should not be used to indicate that an operator or method is not meant to be supported at all – in that case either leave the operator / method undefined or, if a subclass, set it to [None](https://docs.python.org/3/library/constants.html#None).

In fact, the use cases for `NotImplementedError` are:
> In user defined base classes, abstract methods should raise this exception when they require derived classes to override the method, or while the class is being developed to indicate that the real implementation still needs to be added.

In PyCharm (and maybe other python code checkers), this leads to a warning for every sub-class of Metric, saying that all abstract methods should be implemented (PyCharm understands a method that raises a `NotImplementedError` as abstract, even if there is no `@abstractmethod` decorator on this method).

Was there a good reason to define `__iter__` like that? Otherwise, could we remove it?
