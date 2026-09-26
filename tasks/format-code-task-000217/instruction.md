# Support local (inline) IIIF manifests without fetching them

Right now every manifest Mirador knows about is identified by a URL and is
loaded by fetching that URL over the network. We're adding the ability to hand
Mirador a manifest whose JSON we *already have in memory* (for example, a
manifest that was generated locally or read from a dropped file) and have it be
used directly — no network request should ever be made for it.

Please wire this through the relevant parts of the application state so the
following behaviors hold.

## Adding a resource to the catalog

The action creator that adds a manifest to the resource catalog currently takes
only a manifest id. Extend it so that, in addition to the id, a caller may pass
(in this order) the manifest's JSON and an object of extra properties to record
on the catalog entry.

- When extra properties are supplied (e.g. `{ provider: 'file' }`), they must be
  merged onto the stored catalog entry alongside its `manifestId`.
- Adding a resource with only an id must keep storing exactly `{ manifestId }`
  for that entry — no empty/`undefined` extra fields leaking in.
- The existing catalog behavior is otherwise unchanged: entries are prepended
  (most-recent first) and de-duplicated by `manifestId`.
- When the manifest's JSON is supplied while adding a resource, that JSON must be
  stored for the manifest directly and **no network request may be issued** for
  it. When no JSON is supplied, the manifest is fetched exactly as before.

## Opening a window

The action creator that opens a window should accept an optional `manifest` (the
manifest's JSON) among its options. When a window is opened with an inline
`manifest`, that JSON must be stored for the window's manifest directly and **no
network request may be issued** for it. Opening a window without an inline
manifest must keep fetching the manifest as before (and must still skip the
fetch when the manifest is already available).

## Not re-fetching local manifests in the resource list

A resource list item that represents a locally-supplied manifest — identified by
a `provider` of `'file'` — must not kick off a manifest fetch when it appears.
Items without that provider keep their current behavior (they fetch the manifest
when it isn't already loaded/loading/errored).

Nothing about the public shapes of the resulting Redux state (the catalog array
entries, the stored manifest JSON) should change beyond what is described above.
