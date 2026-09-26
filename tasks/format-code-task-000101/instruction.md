### Distinguish permission-denied failures from generic failures via exit code

When `gcs-fetcher` fails because the service account doesn't have permission to read from the source bucket (e.g. missing Storage Object Viewer on the bucket, or VPC-SC blocking access), it exits with the same exit code as any other failure (network blip, checksum mismatch, etc.).

From the outside there is no way to tell these two situations apart. In our build pipeline we'd like to react differently:

- If it's a permission/config problem, the build should fail fast and surface a clear "fix your IAM" message to the user — retrying is pointless.
- If it's a transient/other error, we want to retry or fall through to our normal failure handling.

Right now both cases just give us a non-zero exit and we have to scrape stderr to guess which one happened, which is brittle.

It would be very useful if `gcs-fetcher` used a dedicated exit code when the underlying cause is a GCS permission-denied error, distinct from the generic-failure exit code. This should apply regardless of which source type is being fetched (Manifest, ZipArchive, TarGzArchive) — today only the manifest path even prints the helpful "Access to bucket … denied" message before exiting, and even there the exit code is indistinguishable from any other error.

It would help if the new permission-denied exit code were exposed as a package-level variable (something like `permissionDeniedExitStatus`) so callers and tests can reference it by name.
