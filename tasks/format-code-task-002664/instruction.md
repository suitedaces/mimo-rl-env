### Feature request: gzip-compress uploaded asset files

I've been using linkding's asset feature to attach PDFs and HTML pages to my bookmarks. After importing a fairly large number of bookmarks with attachments, I noticed that the asset folder is taking up significantly more disk space than I expected.

Looking at what's on disk:

- HTML snapshots created by linkding (via the SingleFile integration) are stored gzip-compressed — the files end in `.html.gz` and are pretty small.
- Files I upload manually as assets are stored as-is. A 5 MB HTML page I uploaded stays 5 MB on disk, even though the same page captured as a snapshot would be a fraction of that.

It would be great if uploaded assets were treated the same way as snapshots and got compressed automatically when they're saved. The `BookmarkAsset` model already has a `gzip` flag and the rest of the codebase seems to handle compressed assets fine (downloads, etc.), so it feels like uploads are just inconsistent with the rest.

One thing to keep in mind: people occasionally upload files that are already gzipped (e.g. a `.tar.gz` or some pre-compressed dump). It wouldn't make sense to gzip those a second time, so the auto-compression should only kick in when the upload isn't already gzip.

Thanks!
