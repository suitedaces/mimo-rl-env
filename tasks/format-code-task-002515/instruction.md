# Single-file reader filesystem should support nested paths

restic can back up data read from a stream (for example, `backup --stdin`) by wrapping
the stream in a small read-only filesystem that presents it as exactly one named file.
That filesystem is the `fs.Reader` type in `internal/fs`: you hand it a name, an
`io.ReadCloser` and some metadata, and it implements the `fs.FS` interface on top of it.

Today it only really works when the file lives directly in the root directory. As soon as
the configured name contains directories (e.g. `/path/to/foobar`), the filesystem becomes
inconsistent: `Lstat` happily reports the intermediate directories, but the directory
listings still pretend the file sits at the root, and the intermediate directories can't be
opened at all. Please make `fs.Reader` behave as a coherent virtual filesystem for a single
file located at an arbitrary path (absolute or relative).

The observable behavior should be:

- The file is reachable through both `Open` and `OpenFile` using its full path, and reading
  it yields the stream's bytes. As today, the underlying stream can only be consumed once.

- Every directory on the route from the root down to the file's parent can be opened and
  listed (`Readdir` / `Readdirnames`). Each such directory contains exactly one entry: the
  next element on the path toward the file. The names returned for entries are base names
  (not full paths).

- In directory listings and via `Lstat` / `Stat`, every intermediate path element is reported
  as a directory with mode `os.ModeDir | 0755`, and the final element is reported as the file
  with its configured mode, size and modification time. Names reported are base names.

- The root directory is openable and stat-able both as `"/"` and as `"."`, for both absolute
  and relative file names.

- `Lstat` / `Stat` of a path that is neither the file nor one of its ancestor directories
  returns `os.ErrNotExist`. `Open` / `OpenFile` of such a path returns an error.

- A flat file name (no directories) keeps the current behavior: the file appears directly in
  the root directory listing.
