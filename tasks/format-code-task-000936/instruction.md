Generate-plugin template uses incorrect  Fastify version
### Prerequisites

- [x] I have written a descriptive issue title
- [x] I have searched existing issues to ensure the bug has not already been reported


### Fastify version

5.0.0

### Plugin version

5.0.0

### Node.js version

22.12.0

### Operating system

Linux

### Operating system version (i.e. 20.04, 11.3, 10)

Ubuntu 24.04

### Description

When launch generate-plugin create a nwe plugin it force the fastify version to ^4.0.0 while the fastfy version used is ^5.0.0

### Link to code that reproduces the bug

https://github.com/gafreax/fastify-cli-incorrect-plugin-fastify-version

### Expected Behavior

When using the `fastify generate-plugin` command, the generated plugin
  template specifies a dependency on Fastify version `^4.0.0`.  However, my
  project uses Fastify `^5.0.0` (or higher).  This version mismatch leads to
  errors during plugin installation and prevents the generated plugin from
  working correctly with my existing application.

    To reproduce:

    1. Run `fastify generate-plugin <plugin-name>`
    2. Observe the `package.json` file of the newly generated plugin.  It will
  contain `fastify@^4.0.0` as a dependency.

The error is:

```
> fastify start -w -l info -P app.js

FastifyError [Error]: fastify-plugin: index-auto-0 - expected '^4.x' fastify version, '5.2.1' is installed
    at Object.checkVersion (/home/gafz/Workspace/ex/node_modules/fastify/lib/pluginUtils.js:125:11)
    at Object.registerPlugin (/home/gafz/Workspace/ex/node_modules/fastify/lib/pluginUtils.js:148:16)
    at Boot.override (/home/gafz/Workspace/ex/node_modules/fastify/lib/pluginOverride.js:28:57)
    at Boot._loadPlugin (/home/gafz/Workspace/ex/node_modules/avvio/boot.js:425:25)
    at process.processTicksAndRejections (node:internal/process/task_queues:90:21) {
  code: 'FST_ERR_PLUGIN_VERSION_MISMATCH',
  statusCode: 500
}
```
