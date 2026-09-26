# Add an RSS ingest provider

Superdesk can ingest content from a number of external sources (Reuters, AFP, FTP, …).
Each source type is implemented as an ingest provider that the rest of the system
can look up by a short type name and ask to fetch new content.

We want to add support for ingesting plain **RSS 2.0** feeds.

## What to build

Add a new ingest provider registered under the type name `rss`. Once the
application's installed components are loaded, the provider must be discoverable
through the ingest provider registry (i.e. it shows up among the available /
allowed ingest provider types, just like the existing ones).

The provider is driven by the `config` dictionary stored on a provider record.
The relevant keys are:

- `url` – the feed URL (required)
- `auth_required` – boolean; whether the feed needs HTTP basic authentication
- `username`, `password` – credentials, used only when `auth_required` is true

### Fetching and updating

Asking the provider to update a given provider record must fetch the feed over
HTTP from the configured `url` and return the new content items. When
`auth_required` is true, the HTTP request must carry the `username`/`password`
as basic-auth credentials; otherwise no credentials are sent.

The update result is a list of *batches*; for an RSS feed there is exactly one
batch, i.e. the result is a list whose single element is the list of newly
created content items.

An item is considered **new** when its update/publication time is strictly later
than the provider record's `last_updated` value. If a provider record has no
`last_updated`, every entry in the feed is treated as new. Items are returned in
the order they appear in the feed.

### Content items

Each new feed entry is turned into a content item (a dict) with at least:

- `guid` – the feed entry's guid
- `type` – the string `"text"`
- `headline` – the entry title
- `abstract` – the entry summary/description
- `firstcreated` – the entry's publication time, as a UTC datetime
- `versioncreated` – the entry's update time, as a UTC datetime

### Error handling

When the HTTP request comes back unsuccessful, map the response status to an
`IngestApiError`:

- `401` or `403` → an authorization error, carrying code `4007`
- `404` → a not-found error, carrying code `4006`
- any other unsuccessful status → a general/unknown API error, carrying code `4000`

Any other failure while fetching or reading the feed (for example a
transport-level error or otherwise unusable feed data) must be surfaced as a
`ParserError` instead of letting the raw exception escape.
