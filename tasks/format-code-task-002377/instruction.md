Extra.Forbid is not applied when using BaseSettings with Config.env_file defined
### Initial Checks

- [X] I have searched GitHub for a duplicate issue and I'm sure this is something new
- [X] I have searched Google & StackOverflow for a solution and couldn't find anything
- [X] I have read and followed [the docs](https://pydantic-docs.helpmanual.io) and still think this is a bug
- [X] I am confident that the issue is with pydantic (not my code, or another library in the ecosystem like [FastAPI](https://fastapi.tiangolo.com) or [mypy](https://mypy.readthedocs.io/en/stable))


### Description

Reading the documentation and as BaseSettings inherits from BaseModel it'd be expected to have `Config.extra` parameters working when `Config.env_file` is defined.

It appears that without Config.env files it works as expected, but when it comes from env_files the extra config is ignored.

If this is expected I can make a PR to make the documentation more explicit on this specific point.



### Example Code

```Python
from pydantic import BaseSettings, Extra

""""
# .env.test
title="cool stuff"
other=42
"""

class Plop(BaseSettings):
    title: str

    class Config:
        extra: Extra = Extra.forbid
        env_file = ".env.test"

Plop()
```


### Python, Pydantic & OS Version

```Text
pydantic version: 1.10.2
            pydantic compiled: True
                 install path: .venv/lib/python3.11/site-packages/pydantic
               python version: 3.11.0 (main, Oct 24 2022, 19:55:51) [GCC 9.4.0]
                     platform: Linux-5.17.0-051700-generic-x86_64-with-glibc2.31
     optional deps. installed: ['dotenv', 'typing-extensions']
```


### Affected Components

- [ ] [Compatibility between releases](https://pydantic-docs.helpmanual.io/changelog/)
- [X] [Data validation/parsing](https://pydantic-docs.helpmanual.io/usage/models/#basic-model-usage)
- [ ] [Data serialization](https://pydantic-docs.helpmanual.io/usage/exporting_models/) - `.dict()` and `.json()`
- [ ] [JSON Schema](https://pydantic-docs.helpmanual.io/usage/schema/)
- [ ] [Dataclasses](https://pydantic-docs.helpmanual.io/usage/dataclasses/)
- [ ] [Model Config](https://pydantic-docs.helpmanual.io/usage/model_config/)
- [ ] [Field Types](https://pydantic-docs.helpmanual.io/usage/types/) - adding or changing a particular data type
- [ ] [Function validation decorator](https://pydantic-docs.helpmanual.io/usage/validation_decorator/)
- [ ] [Generic Models](https://pydantic-docs.helpmanual.io/usage/models/#generic-models)
- [ ] [Other Model behaviour](https://pydantic-docs.helpmanual.io/usage/models/) - `construct()`, pickling, private attributes, ORM mode
- [ ] [Plugins](https://pydantic-docs.helpmanual.io/) and integration with other tools - mypy, FastAPI, python-devtools, Hypothesis, VS Code, PyCharm, etc.
