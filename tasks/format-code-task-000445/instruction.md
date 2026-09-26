## websocket example1 is more verbose than it needs to be, and client/server disagree on the wire format

While going through `topics/web/sockets/example1`, the server-side handler in `main.go` looks more complicated than it should be for a teaching example. It manually allocates a 512-byte buffer, calls `ws.Read` into it, checks `n > 0`, slices the bytes back into a string, builds a `Message`, and then constructs a `json.Encoder` around the connection to write the response. For an introductory websocket sample this is a lot of plumbing, and most of it is exactly the kind of boilerplate the `golang.org/x/net/websocket` package is supposed to spare you from.

While reading through it I also noticed the two sides don't actually agree on the wire format:

- The browser side in `static/app.js` sends the raw input string:
  ```js
  ws.send(val);
  ```
- The server, however, never decodes that as JSON on the way in (it just reads bytes), but then turns around and JSON-encodes the response, and the client side does `JSON.parse(evt.data)` on what comes back.

So the inbound direction is "raw text" and the outbound direction is "JSON", even though everything around it is dressed up like it's a JSON conversation. It's confusing to read as an example — a learner can't tell what the intended convention is.

Two things I'd like to see:

1. Simplify the server handler so it isn't doing manual buffer management and manual JSON encoding when the websocket library can handle that for you. The current shape buries the actual lesson (read a message, transform it, write a message back) under buffer-size and byte-slice noise.
2. Make the client and the server agree: if the response is JSON, the request should be JSON too, so the example is internally consistent and a reader doesn't have to wonder whether the asymmetry is intentional.

The externally visible behavior should stay the same — the browser types a string, the server echoes back a `Message` with `original`, `formatted` (uppercased), and `received`, and the page renders it. This is purely about making the example shorter and self-consistent.
