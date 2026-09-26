# Fix the request argument-parsing helpers

Our web layer parses incoming request data with a small set of decorators built
on top of webargs + marshmallow. They live in the web "args" module and are the
single entry point every request handler uses to read and validate query
strings, form data and JSON bodies:

- `use_args` / `use_kwargs`
- `use_rh_args` / `use_rh_kwargs`

These helpers no longer work with the versions of webargs and marshmallow the
project now depends on — importing the module already fails. Reimplement them so
they work again, keeping the public behavior described below. Each decorator
accepts either a marshmallow `Schema` subclass **or** an "argmap" (a plain dict
mapping field names to marshmallow fields), plus keyword arguments, and wraps a
handler function. `use_args`/`use_rh_args` inject the parsed data as a single
positional argument; `use_kwargs`/`use_rh_kwargs` spread it into keyword
arguments.

The observable contract:

- **Whitespace stripping.** Surrounding whitespace is stripped from every parsed
  string value, including strings nested inside lists, regardless of whether the
  data came from the query string, form data or a JSON body. Non-string values
  are untouched, and list/collection structure is preserved.

- **Default location.** When no explicit location is given, arguments are read
  from the request body (form data or JSON), *not* from the query string. A
  handler with no location specified must therefore ignore query-string
  parameters.

- **Unknown fields are ignored.** Input fields that the schema does not declare
  are silently dropped instead of producing a validation error.

- **Validation errors.** A failed validation aborts with the framework's
  standard `422 Unprocessable Entity`. The error payload's `messages` must be a
  flat mapping of `field name -> list of errors`; it must **not** be wrapped in
  an extra layer keyed by the input location.

- **Forwarding options.** Standard webargs parsing options passed as keyword
  arguments — the target `location`, an explicit request object, how unknown
  fields are treated, custom validation, error status/headers — are forwarded to
  the underlying parser. All of webargs' input locations (`query`, `form`,
  `json`, `view_args`, `headers`, `cookies`) work.

- **Schema kwargs / partial.** Keyword arguments meant for the schema
  constructor (e.g. `partial=True` for PATCH-style endpoints) are passed through
  to the schema.

- **Schema context.** A `context` mapping may be supplied and is made available
  to the schema's fields. For `use_rh_args`/`use_rh_kwargs`, the context is
  additionally populated from attributes of the current request handler
  (`flask.g.rh`): for a schema class the attribute names come from its
  `Meta.rh_context`, and for an argmap they come from a required `rh_context`
  keyword argument.

- **Misuse errors.**
  - Passing a schema *instance* (rather than a class or an argmap) to any of the
    four decorators raises `TypeError` whose message starts with
    `Pass a schema or an argmap`.
  - Passing the `rh_context` keyword argument together with a schema *class*
    (instead of an argmap) to `use_rh_args`/`use_rh_kwargs` raises `TypeError`
    with the message `The \`rh_context\` kwarg is only supported when passing an argmap`.
