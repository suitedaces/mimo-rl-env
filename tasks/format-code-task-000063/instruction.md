ioredis package is logging AUTH commands
**Describe the bug**
ioredis instrumentation is logging all commands to redis including the `AUTH` command which contains the password.

https://github.com/DataDog/dd-trace-js/blob/v0.36.2/packages/datadog-plugin-ioredis/src/index.js#L13

**Environment**

* **Operation system:** Linux
* **Node version:** 14.17.5
* **Tracer version:** 0.36.2
* **Agent version:** 7.31.0
