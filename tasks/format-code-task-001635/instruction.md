## POST with nested sub-resources fails with `TypeError: unhashable type: 'dict'`

I'm using Flask-Restless to expose a couple of SQLAlchemy models that have a one-to-many relationship between them, and I'd like clients to be able to create the parent and its children in a single POST instead of having to make a request per resource and then a third one to wire them together.

Roughly, my models look like this:

```python
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    computers = relationship('Computer', backref='owner')

class Computer(Base):
    __tablename__ = 'computer'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    person_id = Column(Integer, ForeignKey('person.id'))
```

Both are registered with the API manager as usual (POST allowed for both). I then send a request like:

```http
POST /api/person
Content-Type: application/json

{
  "name": "Alice",
  "computers": [
    {"name": "laptop"},
    {"name": "desktop"}
  ]
}
```

I expected this to create the `Person` together with the two `Computer` rows attached to it (and similarly to be able to PATCH a person and replace / extend its computers in one go). Instead, the request fails and the server logs

```
TypeError: unhashable type: 'dict'
```

The same thing happens with PATCH when I include a nested list of sub-resource dicts in the body, and also when the relationship is to-one and I send a single nested object instead of a list.

If I instead POST the children separately first and then POST the parent referring to them by id, everything works — so it really does look like the POST/PATCH path doesn't know how to deal with nested resource payloads and ends up trying to use the inner dicts as if they were plain column values.

It would be great if Flask-Restless could accept nested sub-resource payloads on POST/PATCH directly and turn them into the appropriate related model instances (creating new ones or reusing existing ones when a primary key is provided), for both list-valued and scalar relationships.
