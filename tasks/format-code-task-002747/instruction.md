## `disconnect()` is missing on the mock client

I'm using `ioredis-mock` as a drop-in replacement for `ioredis` in my test suite. My application code creates a Redis client, does its work, and then calls `.disconnect()` on it during cleanup. Pretty standard pattern.

Against a real `ioredis` client this works fine. Against `ioredis-mock` the test blows up at the disconnect call — the method just isn't there on the mock, so I get a "not a function" failure and nothing past that point in the teardown runs.

Would be great if the mock supported `disconnect()` so the same code can run against either client without having to branch on whether we're in a test.
