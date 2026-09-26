## Object properties (Content-Type, Cache-Control, custom metadata, ...) are lost after editing a file through gcsfuse

I've been using gcsfuse to mount a bucket where the objects already have meaningful properties set on them — things like `Content-Type`, `Cache-Control`, `Content-Encoding`, plus a few custom metadata entries we use for tracking.

### What I'm seeing

1. Upload an object to the bucket with properties set (via the console / gsutil / API). For example a `.html` file with `Content-Type: text/html`, `Cache-Control: public, max-age=3600`, and a custom metadata pair like `owner=alice`.
2. Mount the bucket with gcsfuse and edit that file through the mountpoint (any modification — append, rewrite, whatever ends up syncing a new generation).
3. Go look at the object again in the GCS console.

After step 3, the only metadata still present is the `gcsfuse_mtime` key that gcsfuse itself writes. `Content-Type` has reverted to the default, `Cache-Control` is gone, and my custom metadata entries are gone too.

### What I expected

Editing a file through the mount shouldn't silently wipe out the object's existing properties. The new generation should carry over whatever was set on the previous generation; gcsfuse is the one writing the new version, so it owns preserving that state. Only the mtime is something gcsfuse legitimately needs to update on its own.

This affects both flows that produce a new generation — full rewrites of small/changed files, and the compose-based "append" optimization for larger files. In both cases the resulting object comes back stripped.

Could the syncer be fixed so that the properties on the source object are retained on the new generation it writes?
