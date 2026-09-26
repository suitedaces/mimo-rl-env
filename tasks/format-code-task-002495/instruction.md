## External version HTML files are showing up in search results and "random page"

We recently started getting builds for pull/merge requests (External Versions), and I noticed that pages from those temporary PR builds are leaking into places where only "real" versions should appear:

1. **Random page redirect** (`/random/` and `/random/<project>/`): hitting this sometimes lands me on a page that belongs to a PR build instead of a branch/tag of the project. PR builds are transient and tied to an unmerged change, so they really shouldn't be picked as the target of a random redirect.

2. **Search index**: the Elasticsearch `PageDocument` index is also picking up HTML files from External Versions. That means searching the docs can return hits that point at PR preview builds, which is confusing — users expect search to cover the project's actual published versions (branches, tags, latest), not in-flight pull requests.

In both places we're going through `HTMLFile.objects` to enumerate the pages, and right now that queryset doesn't distinguish between files that came from a normal version build and files that came from an external (PR/MR) build, so the external ones get mixed in.

Could we make sure these two entry points only consider HTML files from internal versions? It would also be useful if `HTMLFile.objects` exposed a convenient way to ask for "files from internal versions only" / "files from external versions only", since this distinction is going to come up in more places as the External Versions feature gets used.
