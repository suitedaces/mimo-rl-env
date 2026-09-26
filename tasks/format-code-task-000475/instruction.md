Way to reset data-react-beautiful-dnd-draggable for server side rendering
## Bug or feature request?
Bug

### Expected behavior
`data-react-beautiful-dnd-draggable` shouldn't increment based on how many times it was run on the server but start fresh for each request.

### Actual behavior
Each time the server render is hit `data-react-beautiful-dnd-draggable` is incremented by 1.
i.e. after 6 reloads console throws:
```
Warning: Prop `data-react-beautiful-dnd-draggable` did not match. Server: "6" Client: "0"
```

### Steps to reproduce
Server side render and reload couple times, each reload the `data-react-beautiful-dnd-draggable` gets incremented by 1.

### Browser version
Chrome

https://github.com/atlassian/react-beautiful-dnd/blob/master/src/view/style-marshal/style-marshal.js#L11

Possible solution to this would be to expose a function that resets the counter that one could call during a server side render like so:
```
export function resetCounter() {
    count = 0;
}
```
