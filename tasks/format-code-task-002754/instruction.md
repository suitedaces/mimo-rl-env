## Uploaded images don't show thumbnails in the Media Library (local provider)

I'm running a fresh Strapi project with the default upload provider (local, files stored under `/uploads`). After uploading an image through the Media Library, the asset card for that image stays blank — the thumbnail never renders. The card frame, filename, and metadata show up fine, but where the image preview should be there's just empty space (or a broken-image placeholder, depending on the browser).

### Steps to reproduce

1. Start a Strapi project with the default local upload provider.
2. Open the admin panel and go to the Media Library.
3. Upload any image (PNG / JPG, doesn't matter).
4. Look at the resulting asset card in the grid.

Expected: the thumbnail of the uploaded image is visible on the card, like it used to be.

Actual: the card renders but the image area is empty. The page itself doesn't crash, but the dev console shows errors coming from the Media Library code while it tries to render the card. Refreshing the page doesn't help — the thumbnails stay broken as long as the assets are served as relative paths (which is what the local provider does by default).

### Notes

- If I switch to a provider that returns fully-qualified absolute URLs for uploaded files (e.g. an S3-style provider with a public base URL), thumbnails render correctly. So this only seems to affect setups where the upload provider returns a path relative to the Strapi backend, which includes the out-of-the-box local provider.
- This makes the Media Library essentially unusable in any default `create-strapi-app` install — you can upload files, but you can't see what you uploaded.

Would be great if the Media Library could handle both kinds of URLs that an upload provider might return, so the default install just works.
