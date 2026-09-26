Replace `total_ordering` usage with comparison functions implementation
### Is your proposal related to a problem?

We have two instances of `total_ordering` usage within the codebase:

https://github.com/wagtail/wagtail/blob/cd5200c8e1ac0d7299fd9c398b2b994606b3c7d2/wagtail/admin/search.py#L12-L13

https://github.com/wagtail/wagtail/blob/cd5200c8e1ac0d7299fd9c398b2b994606b3c7d2/wagtail/admin/widgets/button.py#L11-L12

Even though it's convenient, `total_ordering` is known to be slow. According to [Python's docs](https://docs.python.org/3/library/functools.html#functools.total_ordering):

> **Note**
> While this decorator makes it easy to create well behaved totally ordered types, it does come at the cost of slower execution and more complex stack traces for the derived comparison methods. If performance benchmarking indicates this is a bottleneck for a given application, implementing all six rich comparison methods instead is likely to provide an easy speed boost.

Django recently removed their usage of `total_ordering` in https://github.com/django/django/pull/16958/commits/ee36e101e8f8c0acde4bb148b738ab7034e902a0 (probably not all usages, I haven't checked).

### Describe the solution you'd like

<!--
  Provide a clear and concise description of what you want to happen.
-->

Replace `total_ordering` with implementations of `__eq__()`, `__ne__()`, `__lt__()`, `__le__()`, `__gt__()`, and `__ge__()`.

### Describe alternatives you've considered

<!--
  Let us know about other solutions you've tried or researched.
-->

Keep using `total_ordering`

### Additional context

I found this while fixing an incorrect import of `total_ordering` in #10525.
