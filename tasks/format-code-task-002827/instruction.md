Annotate `@extend_schema` to accept a list of integers
I'd roughly like to express that my API endpoint directly accepts a list of integers (in my case they will be a list of IDs in the POST body to operate on). The input to the endpoint would look like:

```json
[1, 2, 3, 4]
```

What I roughly would like to do is:

```py
from rest_framework.fields import IntegerField, ListField

class IdListField(ListField):
    child = IntegerField()

@extend_schema(request=IdListField)
def f():
    ...
```

but a `ListField` isn't an actual `Serializer`.

I also tried

```py
@extend_schema(request=list[int])
def f():
    ...
```

But both print out the warning

```
Warning [MyViewSet]: could not resolve request body for POST /api/. Defaulting to generic free-form object. (Maybe annotate a Serializer class?)
```

I think this is similar to Pydantic'c concept of a `RootModel`

- https://docs.pydantic.dev/latest/concepts/models/#rootmodel-and-custom-root-types

Is there a way to express this to `drf-spectacular`?
