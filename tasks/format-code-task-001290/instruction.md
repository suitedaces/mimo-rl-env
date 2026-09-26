# Model Go's `net/smtp` email API for data-flow analysis

Our Go data-flow library can already recognise many "interesting" data sinks
(SQL queries, OS commands, HTTP responses, …), but it currently has no notion
of *email*. As a result, security queries can't reason about untrusted data
that ends up inside an outgoing message. I'd like to add first-class support
for this.

Please extend the library so that it understands data that becomes part of an
email sent through Go's standard `net/smtp` package. Concretely, expose a
data-flow node class named `MailData` — a subclass of `DataFlow::Node`,
reachable from the library's top-level `go` import — whose instances are
exactly the nodes that carry data written into an email (its headers or body).

A node should be a `MailData` node in the following situations:

- **`smtp.SendMail(addr, a, from, to, msg)`** — the message argument (`msg`,
  the byte slice holding the email body) is email data. The relevant node is
  that argument expression as written at the call site.

- **The streaming API via `(*smtp.Client).Data()`** — `Data()` returns an
  `io.WriteCloser` representing the email message; anything written to that
  writer is email data. Specifically, when the returned writer is passed as the
  destination (first argument) of a call to `io.WriteString` or `fmt.Fprintf`,
  every *other* argument of that write call (the string written, or the format
  string together with each formatted value) is a `MailData` node. This must
  keep working when the writer is first stored in a local variable and then
  used in the write call.

Notes / expectations:

- Static, constant data still counts — whether the body is built from a literal
  or from a variable, the argument node is reported. Identifying *untrusted*
  data is the job of a separate query; this change is purely about marking where
  email data flows.
- The modelling should be open for extension: adding support for further
  email-sending APIs later should not require rewriting what's already there.
- Make sure the new class is wired into the library so a query that does nothing
  more than `import go` can refer to `MailData`.
