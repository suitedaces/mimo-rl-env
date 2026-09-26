'path can't be empty'
When mounting only a router created with `MosaicTilerFactory` without any prefix, FastAPI will error with `"Exception: Prefix and path cannot be both empty (path operation: read)"`

https://github.com/developmentseed/titiler/blob/f2821b9421ecad0e1a79356fc82c3f6ee39833f5/titiler/endpoints/factory.py#L720-L725

This will be a **breaking change** for the application that are already build on top of titiler

In order to make a smooth transition we could maybe do 
```python
@self.router.get(
    "",
    response_model=MosaicJSON,
    response_model_exclude_none=True,
    responses={200: {"description": "Return MosaicJSON definition"}},
    deprecated=True,
)
@self.router.get(
    "/",
    response_model=MosaicJSON,
    response_model_exclude_none=True,
    responses={200: {"description": "Return MosaicJSON definition"}},
)
```
