## ChoiceType with a Python Enum class doesn't work

`sqlalchemy_utils.ChoiceType` supports two forms for its `choices` argument:
either a list of `(value, label)` tuples, or a Python `enum.Enum` subclass.
The tuple form works fine with graphene-sqlalchemy, but if I pass an Enum
class, the auto-generated GraphQL schema breaks.

Minimal example:

```python
import enum
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types.choice import ChoiceType
from graphene_sqlalchemy import SQLAlchemyObjectType

Base = declarative_base()

class Status(enum.Enum):
    active = 1
    inactive = 2

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    # tuple form -- works
    # status = Column(ChoiceType([(1, 'active'), (2, 'inactive')]))
    # enum form -- blows up
    status = Column(ChoiceType(Status, impl=Integer()))

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
```

Switching `status` to the tuple form makes everything work, so the Enum
form of `ChoiceType` seems to be the part that's not handled. It would be
nice if both forms produced an equivalent GraphQL Enum, since the docs for
`ChoiceType` advertise Python Enum classes as a first-class option.
