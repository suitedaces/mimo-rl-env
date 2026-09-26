# Avatar image helpers for profile uploads

We're building out profile-image uploads for the user settings screens. The UI needs two small,
well-tested helpers to deal with avatars, and right now they don't exist. Please add them as
utilities under `src/utils`.

## 1. `sanitizeAvatars(file, fallbackUrl)`

Export a function `sanitizeAvatars` from `src/utils/sanitizeAvatar.ts` with the signature
`(file: File | null, fallbackUrl: string) => string`. It decides what image source to show:

- If `file` is a real `File` whose MIME type is an image (its `type` starts with `image/`), return
  an object URL created from that file (i.e. the result of `URL.createObjectURL(file)`).
- Otherwise (the file is `null`, or it is not an image), fall back to `fallbackUrl`:
  - Resolve `fallbackUrl` as a URL against the current page origin (`window.location.origin`) and
    return the resulting normalized absolute URL string. A relative path like `/avatar.jpg` must
    become an absolute URL under the current origin; query strings and fragments must be preserved;
    non-ASCII characters end up percent-encoded as part of normalization.
  - If `fallbackUrl` is missing/empty or cannot be parsed into a valid URL, log an error to
    `console.error` and return an empty string `''`.

The function must never throw.

## 2. `urlToFile(url)`

Export an async function `urlToFile` from `src/utils/urlToFile.ts` with the signature
`(url: string) => Promise<File>`. It downloads a remote image so it can be re-uploaded as multipart
form data:

- Fetch the given `url` and read the response body as a `Blob`.
- Return a `File` built from that blob. The file's `type` is the blob's MIME type. The file's name
  is the URL's final path segment, or `avatar` when the URL has no final segment (e.g. it ends in a
  slash), followed by a dot and the extension taken from the blob's MIME subtype (the part after the
  `/`). For example a blob of type `image/png` fetched from a URL ending in `/` produces a file
  named `avatar.png`.
- If anything goes wrong (the fetch rejects, or reading the blob rejects), log the error to
  `console.error` and re-throw it so the caller's promise rejects with the same error.
