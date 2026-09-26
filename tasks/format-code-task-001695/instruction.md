Use of functools.lru_cache makes scifit-fem objects un-pickle-able
I have an application where I run multiple FE problems at once using the `multiprocess` library.  Internally this library uses `dill` to pickle to the objects to pass them off to the new processes.  In the past this worked fine, but the recent update uses `functools.lru_cache` to cache calls for the mapping jacobian

https://github.com/kinnala/scikit-fem/blob/bc57d968e56e6b89a99e35eac26ef7bc81b7a46a/skfem/mapping/mapping_isoparametric.py#L64

This decorator makes the object un-pickle-able, breaking multiprocessing in my application.

I suggest providing an option to turn off/not use caching to support being able to pickle scikit-fem objects.
