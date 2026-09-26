### s3manager.Upload API shape — align with upcoming Download manager

I'm working on adding a download manager to `s3manager` (counterpart to the existing upload manager). While sketching the API I realized the two are going to look inconsistent if I leave Upload as-is.

Today, uploading looks like this:

```go
svc := s3.New(nil)
resp, err := s3manager.Upload(svc, &s3manager.UploadInput{...}, nil)
```

i.e. `Upload` is a package-level function that takes the `*s3.S3` client, the input, and an options struct as positional arguments. The download manager I'm building really wants to be a reusable object — you configure it once (concurrency, part size, which S3 client to use) and then call it many times against different inputs. Forcing the same shape on Upload would mean every call site has to re-pass the client and the opts, and the two managers would read very differently side by side even though they're conceptually symmetric.

I'd like to reshape Upload along the same lines: configure once, then call `Upload` on the configured object as many times as you want, ideally safe to share across goroutines. The S3 client should be part of that one-time configuration rather than a required positional argument on every call — and it'd be nice if it were optional, so simple use cases (`just upload this file with defaults`) don't have to construct an `s3.S3` themselves.

I'm fine with this being a breaking change for Upload callers — better to do it now, before the download manager ships and locks in the asymmetry, than to introduce two differently-shaped APIs and try to reconcile them later.

The existing knobs in `UploadOptions` (PartSize, Concurrency, LeavePartsOnError) and the zero-value-means-default behavior should keep working the way they do now; this is purely about the call shape, not about changing what the upload itself does.

Naming-wise I'd expect something like `s3manager.NewUploader(opts)` returning the reusable object, with the S3 client living on `UploadOptions` (e.g. an `S3` field).
