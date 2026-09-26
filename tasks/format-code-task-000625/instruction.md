# Add a PagerTree notification service

We'd like Apprise to be able to send alerts to [PagerTree](https://pagertree.com)
through its webhook integration API. Please add a new notification service that is
reachable with the `pagertree://` URL scheme and behaves as described below.

## URL format

```
pagertree://{integration_id}
pagertree://{integration_id}?action=resolve&thirdparty=abc123&urgency=high&tags=prod,server
```

* `integration_id` is the only required component. A valid integration id begins
  with `int_` followed by between 7 and 14 additional characters, each of which
  is a letter, digit, hyphen, or underscore. If the integration id is missing or
  does not satisfy this pattern, constructing the object must raise a `TypeError`.
* `thirdparty` (optional) — an externally supplied id used to correlate alerts.
  If supplied it must be a non-empty string, otherwise a `TypeError` is raised.
* `action` (optional) — one of `create`, `acknowledge`, or `resolve`. The default
  is `create`. Any value that is not one of these three is ignored and the default
  (`create`) is used instead.
* `urgency` (optional) — one of `silent`, `low`, `medium`, `high`, or `critical`.
  Any other value (or omitting it) means no urgency is sent at all.
* `tags` (optional) — a comma separated list of tags.

The service must also support three kinds of prefixed URL arguments, mirroring the
convention used by other webhook-style services in this project:

* arguments prefixed with `+` are added as **HTTP headers** on the outgoing request,
* arguments prefixed with `:` are merged into the top level of the **JSON payload**,
  overriding any value already there,
* arguments prefixed with `-` are collected into a **`meta`** object inside the payload.

The object's `url()` must round-trip: re-instantiating from the value returned by
`url()` must yield an equivalent service.

## Delivery behavior

A notification performs an HTTP `POST` to
`https://api.pagertree.com/integration/{integration_id}`. The request body is JSON
and the request always carries a `Content-Type: application/json` header (plus any
headers supplied with the `+` prefix, which take precedence).

The JSON body always contains:

* `id` — the `thirdparty` value when one was provided, otherwise a generated,
  non-empty unique identifier (a fresh one per notification).
* `event_type` — the resolved action (`create`, `acknowledge`, or `resolve`).

When (and only when) the action is `create`, the body additionally contains:

* `title` — the notification title, falling back to the application description
  when no title is given,
* `description` — the notification body,
* `meta` — a JSON object built from the `-` prefixed arguments (an empty object
  when none were given),
* `tags` — the list of tags (an empty list when none were given),
* `urgency` — present only when a valid urgency was provided.

For the `acknowledge` and `resolve` actions, none of `title`, `description`,
`meta`, `tags`, or `urgency` are included — only `id`, `event_type`, and whatever
was merged in through `:` prefixed payload arguments.

Any `:` prefixed payload arguments are applied last, so they can add to or override
the fields above.

## Response handling

HTTP responses with a 2xx status code (specifically `200`, `201`, and `202`) are
treated as success and the notification reports success. Any other status code
(for example `402`, `403`, `404`, `405`, or `429`) is treated as a delivery
failure and the notification reports failure. A connection-level error is also a
failure.
