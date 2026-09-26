## Inconsistent file-operation API between `MockTarget` / `MockFileSystem` and the other backends

I'm writing unit tests for a luigi task that renames files. In production the task operates on S3 via `S3Target`, and I'd like to use `MockTarget` / `MockFileSystem` in tests so I don't have to hit S3 (or even disk). I'd also like the task itself to be storage-agnostic via `OpenerTarget` from `luigi.contrib.opener`, so I can point it at `s3://`, a local path, or a mock path depending on context.

The problem is that the file-operation surface exposed by the different `FileSystem` / `FileSystemTarget` implementations isn't consistent, and `MockTarget` / `MockFileSystem` in particular is missing pieces that the other backends have:

- `MockFileSystem` doesn't have `move` or `copy` at all. If my production code calls `target.move(...)` or `fs.copy(...)`, it just works against `LocalTarget` / `S3Target`, but against `MockTarget` it blows up with an attribute error.
- `MockTarget` only exposes `rename`. So my options for testing are either to special-case the test path to call `rename` (which means the test isn't really exercising the same code path as production), or to wrap the mock backend in some adapter — both feel wrong.
- On the `S3Client` side, `rename` and `move` are already interchangeable, which is great, but that convenience isn't reflected on the other backends, so I can't rely on it in code that's meant to be backend-agnostic.

The net effect is that writing tests against `MockTarget` (especially when the production code uses `OpenerTarget` to pick a backend) becomes convoluted and error-prone, because the same call that works fine on one backend doesn't exist on another.

What I'd like is for every backend that inherits from `FileSystem` / `FileSystemTarget` — at minimum `LocalFileSystem`/`LocalTarget`, `MockFileSystem`/`MockTarget`, and `S3Client`/`S3Target` — to present a uniform set of file operations for moving, renaming and copying files, so that storage-agnostic code (including code written through `OpenerTarget`) behaves the same regardless of the underlying backend.
