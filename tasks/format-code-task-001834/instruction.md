# Add an Azure Blob Storage backend to `Arctic`

`Arctic` can currently be pointed at S3 (`s3://` / `s3s://`) and LMDB (`lmdb://`) backends. We want
to add **Azure Blob Storage** as a first-class backend so that users can point `Arctic` at an Azure
storage account using an `azure://` connection URI, exactly the way S3 and LMDB are wired in today.

The piece this task is about is recognising and parsing the `azure://` URI and translating it into
the values the storage layer needs. The new backend must plug into the same machinery the existing
backends use, so that `Arctic` selects it automatically when it is handed an `azure://` URI.

## URI format

```
azure://<key1>=<value1>;<key2>=<value2>;...
```

The body after `azure://` is a list of `<key>=<value>` pairs separated by semicolons (`;`).

Most of these pairs make up the **Azure connection string** that the Azure SDK understands (for
example `DefaultEndpointsProtocol`, `AccountName`, `AccountKey`, `BlobEndpoint`). Three keys are
**not** part of the connection string — they are ArcticDB-specific options:

- `Container` — the name of the blob container to use.
- `Path_prefix` — an optional prefix within the container under which data is stored.
- `CA_cert_path` — an optional path to a CA certificate bundle.

## Required behaviour

- The new backend must be recognised for, and only for, URIs beginning with `azure://`. The existing
  S3 and LMDB backends must keep rejecting `azure://` URIs, and the new backend must reject `s3://`,
  `s3s://` and `lmdb://` URIs. `Arctic` must automatically select the new backend for an `azure://`
  URI without any extra configuration.

- **Connection string translation.** The backend must reconstruct the Azure connection string from
  the URI by taking every `<key>=<value>` pair whose key is *not* one of the three ArcticDB-specific
  options and re-joining them with `;`, **preserving the order in which they appeared** in the URI.
  Values are taken verbatim — a value may itself contain `=` characters (e.g. an account key ending
  in `==`) and must be kept intact. Keys are matched exactly: a connection-string value that merely
  contains the text `Container` (e.g. `AccountName=Containerxyz`) must not be treated as the
  `Container` option.

- **Container.** The value of the `Container` option is exposed as the container name.

- **Path prefix.** The value of `Path_prefix` is exposed, with any leading and trailing `/`
  characters stripped. If `Path_prefix` is not supplied it is `None`. This is surfaced the same way
  the S3 backend surfaces it — through a `path_prefix` property on the backend.

- **Representation.** The backend's `repr()` follows the same convention as the other backends and
  shows the translated connection string and the container, in the form
  `azure(endpoint=<connection string>, container=<container>)`.

- **Validation.** An `azure://` URI whose body is empty (no parameters at all) is invalid and must
  raise `ValueError` when the URI is parsed.

The actual reading from / writing to Azure is handled elsewhere and is out of scope here — this task
is only about recognising the URI scheme and parsing it into the connection string, container and
path prefix described above.
