## Record import: a file decoder for compose

We want to support importing records into compose from uploaded data files. Two
file shapes need to be handled uniformly: **flat** files (CSV-style, where the
first row is a header naming the columns) and **structured** files (JSONL —
one JSON object per line). The rest of the import pipeline shouldn't care which
shape it's dealing with; it just wants to know how many records there are, what
the columns/field names are, and to walk the records turning each one into a
`compose/types.Record`.

Please add a decoder package under `compose/decoder` (import path
`github.com/cortezaproject/corteza-server/compose/decoder`) that exposes two
constructors:

- `NewFlatReader(r, f)` — wraps a row reader `r` whose only requirement is a
  `Read() ([]string, error)` method (a `*csv.Reader` satisfies this) together
  with a seekable handle `f` (`io.ReadSeeker`) to the same raw data.
- `NewStructuredDecoder(d, f)` — wraps a streaming decoder `d` exposing
  `Decode(interface{}) error` and `More() bool` (a `*json.Decoder` satisfies
  this) together with a seekable handle `f` (`io.ReadSeeker`) to the same raw
  data.

Both constructors return a value exposing the same three methods:

- `Header() []string` — the field/column names.
  - For flat input the header is the first physical row, returned in its
    original column order.
  - For structured input there is no dedicated header row; the names are the
    keys of the first object (order is not significant).

- `EntryCount() (uint64, error)` — the number of **data** records in the file,
  determined from the seekable handle and leaving that handle rewound to the
  start afterwards.
  - For flat input the header row is not a data record, so a file with a header
    and N data rows reports N; an empty file reports 0.
  - For structured input every line is a data record (a file with N objects
    reports N).

- `Records(fields map[string]string, create RecordCreator) error` — iterates
  over the data records, builds a `types.Record` for each, and invokes the
  `create` callback once per record (a `RecordCreator` is
  `func(*types.Record) error`). `fields` maps a source column/key name to the
  target record field name.
  - Only the columns/keys present in `fields` are imported; anything else in
    the source is ignored.
  - A target name that matches a known system field is set directly on the
    record struct: `recordID`/`ID` → ID, `moduleID`, `namespaceID`, `ownedBy`,
    `createdBy`, `createdAt`, `updatedBy`, `updatedAt`, `deletedBy`,
    `deletedAt`. (The numeric IDs parse as base-10 unsigned integers; the
    timestamps parse as RFC3339.)
  - Every other target name produces a `types.RecordValue` (with that `Name`
    and the cell's string value) appended to the record's `Values`.
  - If any target name in `fields` is the empty string, importing fails with an
    error and the callback must not be relied upon to have succeeded.

One subtlety: obtaining the header must not consume any data record. After
calling `Header()`, a subsequent full iteration via `Records()` must still visit
every data record — including the first object of a structured file, which is a
real data record even though its keys were used to derive the header.
