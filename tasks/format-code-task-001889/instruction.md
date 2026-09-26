FastifyError [Error]: onGatewayReplaceSchema hook not supported!
Latest update to mercurius v12.0.0 is causing this error, rolling back to 11.5.0 eliminates the error

`
FastifyError [Error]: onGatewayReplaceSchema hook not supported!
    at Hooks.validate (node_modules/mercurius/lib/hooks.js:33:11)
    at Hooks.add (node_modules/mercurius/lib/hooks.js:38:8)
    at fastifyGraphQl.addHook (node_modules/mercurius/index.js:383:18)
    at module.exports.fp.fastify (node_modules/mercurius-cache/index.js:40:15)
    at Plugin.exec (node_modules/avvio/plugin.js:130:19)
    at Boot.loadPlugin (node_modules/avvio/plugin.js:272:10)
    at process.processTicksAndRejections (node:internal/process/task_queues:82:21) {
  code: 'MER_ERR_HOOK_UNSUPPORTED_HOOK',
  statusCode: 500
}
`

Enabled Mercurius Plugins
- Cache
