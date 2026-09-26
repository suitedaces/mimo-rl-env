# Translate Segment destination config into PostHog hog-function config

We're starting to import [Segment](https://segment.com) action destinations into
PostHog's CDP. Segment describes *what* to send using two pieces of config that we
need to convert into the equivalents PostHog already understands:

1. A **subscription / FQL string** that decides which events a mapping fires on.
2. **Field "default" values** that describe where each piece of data comes from,
   written with Segment's directive objects (`@path`, `@if`).

Add a small, dependency-free translation layer for these two pieces. It must live in
the plugin-server CDP code and expose two pure functions from
`plugin-server/src/cdp/segment/segment-templates.ts`:

```ts
translateFilters(subscribe: string): { events: HogFunctionFilterEvent[] }
translateInputs(defaultVal: any, multiple?: boolean): any
```

## `translateFilters`

Segment's FQL talks about event `type`s; PostHog talks about event names. Given a
subscription string, return a single PostHog event filter:

```ts
{
  events: [
    {
      id: 'All events',
      name: 'All events',
      type: 'events',
      order: 0,
      properties: [{ key: <translated string>, type: 'hogql', value: null }],
    },
  ],
}
```

`<translated string>` is the input string after applying these rewrites to **every**
occurrence:

| Segment FQL fragment | PostHog HogQL fragment |
|---|---|
| `type = "page"`     | `event = "$pageview"` |
| `type = "screen"`   | `event = "$screen"` |
| `type = "identify"` | `event in ('$identify', '$set')` |
| `type = "group"`    | `event = "$groupidentify"` |
| `type = "track"`    | `event not in ('$pageview', '$screen', '$alias', '$identify', '$set', '$groupidentify')` |
| `type = "alias"`    | `event = "$alias"` |

After those substitutions, every remaining double quote (`"`) in the string becomes a
single quote (`'`). Fragments not listed above (e.g. a `name = "Order Completed"`
clause joined with `and`/`or`) pass through unchanged apart from the quote conversion.

## `translateInputs`

This resolves a single Segment field default into the string/value PostHog stores for
a hog-function input.

- A `boolean` or `string` default is returned **unchanged**.
- An object with an **`@path`** key: take the path string, replace a leading `$.` with
  `event.`, normalize the field reference (see below), then:
  - if normalization yields an empty string, return `''`;
  - otherwise return it wrapped in PostHog templating braces: `{<value>}`, or
    `{[<value>]}` when `multiple` is `true`.
- An object with an **`@if`** key shaped like `{ exists, then, else }`:
  - Only handle the common "exists check on the same field" case, i.e. when
    `JSON.stringify(exists)` equals `JSON.stringify(then)`. In any other shape, return
    `JSON.stringify(defaultVal)`.
  - Resolve `then` and `else` independently: an `@path` object is converted exactly
    like the `@path` case above but **without** the surrounding braces; a plain string
    is wrapped in single quotes (`'value'`).
  - Combine the resolved primary (`then`) and fallback (`else`):
    - both empty → `''`;
    - primary empty, fallback present → `{<fallback>}`;
    - primary present, fallback empty → `{<primary>}`;
    - both present → `{<primary> ?? <fallback>}`, and when `multiple` is `true` the
      `?? ` expression is wrapped in brackets: `{[<primary> ?? <fallback>]}`.
- Any other object is returned as `JSON.stringify(defaultVal)`.

### Field reference normalization

After the `$.` → `event.` step, field references are rewritten to their PostHog
equivalents. These specific references must be remapped (matching anywhere in the
string):

| Segment reference | PostHog reference |
|---|---|
| `event.traits`         | `person.properties` |
| `event.context.traits` | `person.properties` |
| `event.userId`         | `person.id` |
| `event.anonymousId`    | `event.distinct_id` |
| `event.messageId`      | `event.uuid` |
| `context.os.name`      | `properties.$os` |
| `context.os.version`   | `properties.$os_version` |
| `context.page.url`     | `properties.$current_url` |
| `context.page.path`    | `properties.$pathname` |
| `context.page.referrer`| `properties.$referrer` |
| `context.campaign.source` | `properties.utm_source` |
| `context.ip`           | `properties.$ip` |
| `context.locale`       | `properties.$locale` |
| `context.userAgent`    | `properties.$raw_user_agent` |

Some Segment fields have no PostHog equivalent and must be dropped — replaced with an
empty string. These include `context.device.brand`, `context.network.wifi` and
`context.device.advertisingId`; when one of these is the whole reference, the value
resolves to `''`.

General rule applied after the specific remaps:

- If, after all rewrites, the value ends with a `.`, the field has no usable mapping —
  return `''`.

A reference that matches none of the above (e.g. `event.properties.revenue`, or an
unrecognised `event.context.*` path) passes through unchanged.
