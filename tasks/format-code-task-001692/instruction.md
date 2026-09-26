HyperParameters.get(): should raise KeyError rather than ValueError when name is not Found
Let ``hp`` be an empty ``HyperParameters`` container. When calling ``hp.get('anything')`` or ``hp['anything']``, a ``ValueError`` is raised. It would be more pythonic if it raised a ``KeyError``.

``HyperParameters`` objects are ``dict``-like containers . A ``dict`` would raise a ``KeyError``.

*keras-tuner version: 1.0.1*
