keyPrefix does not seem to work as expected
The tests for `keyPrefix` don't seem to be valid, and correcting them results in a failure.  In particular, if you have two Redis instances that share the same data, but use a different key prefix, they will interfere with one another.

Here's a test that shows the issue:

```

describe('multiple intance use same key with diffence keyPrefix', () => {
    const redis1 = new MockRedis({
      data: {
        foo: 'bar',
        hello: 'world',
      },
      keyPrefix: 'test:',
    });

    const redis2 = redis1.createConnectedClient({
      keyPrefix: 'test2:',
    });

    it('should return null on keys that do not exist', () =>
      redis2.get('foo').then(result => expect(result).toBe(null)));
```

Here's another example test that fails:

```
  describe('multiple instance use same key with diffence keyPrefix', () => {
    const redisBase = new MockRedis({
      data: {
        foo: 'bar',
        hello: 'world',
      },
    });
    const redis1 = redisBase.createConnectedClient({
      keyPrefix: 'test:',
    });

    const redis2 = redis1.createConnectedClient({
      keyPrefix: 'test2:',
    });

    it('should not be able to read something set with one prefix using another prefix', () =>
      redis2
        .set('hello', 'ioredis')
        .then(status => expect(status).toBe('OK'))
        .then(() => redis1.get('hello'))
        .then(result => expect(result).toBe(null)));
  });
```

The current test suite uses separate instances of `MockRedis` and tests that they do not interfere.  However, each instance of `MockRedis` already will not interfere, that's how `MockRedis` works!  To only way to test that a `keyPrefix` results in non-interference between instances is to use `createConnectedClient` as above.
