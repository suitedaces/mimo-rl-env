Adding `.as` method to collection items?
When testing against several items of a collection, the code can be a bit hard to follow. Maybe adding a new helper, like `.as(...)` could help to group and make it easy to spot what's being tested.

Change this

```
andThen(() => {
  assert.equal(page.users(1).name, 'John');
  assert.equal(page.users(1).lastName, 'Doe');
  assert.equal(page.users(1).email, 'john@doe');

  assert.equal(page.users(2).name, 'John');
  assert.equal(page.users(2).lastName, 'Doe');
  assert.equal(page.users(2).email, 'john@doe');

  assert.equal(page.users(3).name, 'John');
  assert.equal(page.users(3).lastName, 'Doe');
  assert.equal(page.users(3).email, 'john@doe');
});
```

to this

```
andThen(() => {
  page.users(1).as(user => {
    assert.equal(user.name, 'John');
    assert.equal(user.lastName, 'Doe');
    assert.equal(user.email, 'john@doe');
  });

  page.users(2).as(user => {
    assert.equal(user.name, 'John');
    assert.equal(user.lastName, 'Doe');
    assert.equal(user.email, 'john@doe');
  });

  page.users(3).as(user => {
    assert.equal(user.name, 'John');
    assert.equal(user.lastName, 'Doe');
    assert.equal(user.email, 'john@doe');
  });
});
```

I'm naming the method `.as(...)` but the inspiration comes from the [ruby method `.tap`](http://ruby-doc.org/core-2.2.3/Object.html#method-i-tap).

What do you think? Would you find it useful?
