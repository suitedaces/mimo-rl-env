# Add a YouTube service

We'd like `libsaas` to talk to Google's YouTube APIs. Please add a new service,
exposed as `libsaas.services.youtube.YouTube`, that wraps both the **Data API
v3** and the **Analytics API v1**.

## Authentication

The service is created from an OAuth2 access token:

```python
service = youtube.YouTube('my-access-token')
```

Every request the service issues — whether to the Data API or the Analytics API
— must carry the bearer token in an `Authorization` header whose value is
`Bearer <access-token>` (e.g. `Bearer my-access-token`).

## Data API v3

The Data API lives under `https://www.googleapis.com/youtube/v3`. The service
must expose read-only accessors for these resources, reachable as methods on the
service object:

- `activities()`
- `channels()`
- `playlists()`
- `videos()`
- `search()`

Each accessor returns a resource whose `get(...)` method performs an HTTP `GET`
against `https://www.googleapis.com/youtube/v3/<resource>` (where `<resource>`
is the accessor name, e.g. `.../youtube/v3/activities`) and parses the response
as JSON.

`get` always takes a required `part` argument plus any number of optional
filtering arguments that the YouTube API understands for that resource (for
example `channelId`, `mine`, `maxResults`, `pageToken`, `id`, `q`, ...). These
arguments are passed straight through as query parameters using the exact names
the YouTube API uses, with two rules:

- An argument that is left unset (`None`) is omitted from the query string
  entirely.
- Boolean arguments are serialized as the strings `'true'` and `'false'`.

These are read-only resources: calling `create`, `update` or `delete` on any of
them must raise `libsaas.services.base.MethodNotSupported`.

## Analytics API v1

The Analytics API is reachable from the service through an `analytics()`
accessor and targets `https://www.googleapis.com/youtube/analytics/v1/reports`.

It provides a single retrieval method:

```python
service.analytics().get(ids, metrics, start_date, end_date,
                        dimensions=None, filters=None, max_results=None,
                        start_index=None, sort=None)
```

This performs an HTTP `GET` against the reports URL and parses the response as
JSON. `ids`, `metrics`, `start_date` and `end_date` are required; the rest are
optional and omitted when left as `None`.

The wrinkle is that the Analytics API names its query parameters with hyphens,
while the method takes Pythonic underscore arguments. Every underscore in an
argument name must become a hyphen in the emitted query parameter, so a call
like:

```python
service.analytics().get('channel==MINE', 'views', '2012-01-01', '2012-03-01',
                        max_results=10, start_index=1)
```

must send query parameters named `start-date`, `end-date`, `max-results` and
`start-index` (and `ids`, `metrics` unchanged). As with the Data API, unset
optional arguments are dropped.

Analytics is also read-only: `create`, `update` and `delete` must raise
`libsaas.services.base.MethodNotSupported`.
