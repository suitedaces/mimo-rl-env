I need to add a way to send messages from workers to main thread:

The only possibility I see right now with Piscina, is to send a messagePort when running a task and use it to communicate (Or use a broadcastChannel but only for node 17+).

In my case, I want to use a single messagePort per worker, set at startup of the worker and use it when initializing inside the worker and before running tasks... But there is no currently easy way to add a messagePort per worker at startup built in Piscina...

I wonder if it would be possible to use the already existing built in messages ports of Piscina to add this feature ?

Something like this:

Adding a new kind of message that the worker can send:
```js
export interface GenericMessage {
  data: any;
}
```

Use it to send messages from worker at any stage:
```js
let message : GenericMessage;
parentPort.postMessage(message);
```

And handle such messages at pool level to expose it:
```js
worker.on('message', (message : GenericMessage) => {
  publicInterface.emit('message', message.data);
}
```

Do this make sense ?
