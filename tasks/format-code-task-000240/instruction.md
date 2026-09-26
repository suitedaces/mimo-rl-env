Add an option to use encrypted connection
Currently to use an encrypted connection the client needs to pass some certificates.
https://github.com/SAP/node-hdb#encrypted-network-communication
If HANA server is using a certificate signed by a public CA like VeriSign, there is no need to pass custom certificates as most public certificates are builtin in node.js. See `ca` optin in [tls.createSecureContext](https://nodejs.org/docs/latest/api/tls.html#tls_tls_createsecurecontext_options).
For such cases it would be useful to have a separate option to enable encryption, e.g.
```js
var client = hdb.createClient({
  host : 'hostname',
  port : 30015,
  ssl: true,
  ...
});
```
Probably a better name should be used as node actually uses TLS.
As a workaround you can pass `ca: undefined`
```js
var client = hdb.createClient({
  host : 'hostname',
  port : 30015,
  ca: undefined,
  ...
});
```
