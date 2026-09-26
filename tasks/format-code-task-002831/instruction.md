Mock SocketIO does not retain protocol
`IO.connect` accepts a second `protocol` argument when creating a socket instance. It appears that `mock SocketIO` implementation allows for a protocol, but the `mocked IO` function does not pass it along. Also, `mock SocketIO` expects protocol to be a string or array but an object is an acceptable input so I think that can be fixed also.

Repro:
```
// implementation.js
const socket = io.connect(URL, 'custom protocol');

// test.js
mockServer.on('connection', (server, clientInstance) => {
  clientInstance.protocol === 'custom protocol'; // This evaluates to false.
});
```
