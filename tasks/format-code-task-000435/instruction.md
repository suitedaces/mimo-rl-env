bug: `SitemapRequestList.persistState()` throws when sitemap loading has finished
If `SitemapRequestList` finishes parsing the remote sitemaps and `persistState()` is called, it throws an exception.

This is because after parsing the sitemaps fully, the `SitemapRequestList` [closes the internal stream with `.push(null)`](https://github.com/apify/crawlee/blob/f3eb99d9fa9a7aa0ec1dcb9773e666a9ac14fb76/packages/core/src/storages/sitemap_request_list.ts#L364).

When `persistState()` is called afterwards, the contents of the stream are read into a (persisted) list. To not mutate the internal state with `persistState()`, we return the stream contents back to the original stream - if the stream had been closed, this causes an exception (push after EOF).
