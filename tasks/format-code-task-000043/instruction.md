# Fix DataFrame uploads with reserved/geometry columns

Uploading a `pandas`/`geopandas` DataFrame to CARTO via `Dataset(df).upload(...)` is
generating inconsistent and sometimes broken SQL. For example, a DataFrame whose only
columns are `cartodb_id` and `the_geom` ends up producing a `CREATE TABLE` statement with
a dangling leading comma like `CREATE TABLE t (, the_geom geometry(...))`, which the
database rejects. The root cause is that the column list used to create the table, the
column list used in the `COPY` statement, and the values written to each row are all
computed independently and can disagree about how many columns there are and what they are
called.

Make the upload path derive a single, consistent description of the destination columns
from the DataFrame and use it everywhere. The observable behavior of an upload (the
`CREATE TABLE` statement and the `COPY ... FROM stdin` statement together with the rows of
CSV data streamed to the backend) must satisfy the following contract.

## Column selection and ordering

- Every column of the DataFrame is uploaded, in the DataFrame's original column order. In
  particular `cartodb_id` is treated as a normal column and is kept.
- A column named `the_geom_webmercator` (matched case-insensitively) is always dropped and
  never appears in the table, the `COPY` column list, or the data.

## Geometry handling

- Exactly one column is treated as the geometry. If the DataFrame is a GeoDataFrame with an
  active geometry column, that column is used; otherwise the first column whose lower-cased
  name is one of `the_geom`, `geom`, `geometry` is used, considered in that order of
  priority (so if several are present, `the_geom` wins, then `geom`, then `geometry`).
- The chosen geometry column is named `the_geom` in the destination, declared with type
  `geometry(<GeometryType>, 4326)` where `<GeometryType>` is detected from the data (e.g.
  `Point`), and its values are emitted as `SRID=4326;<WKT>`. A null/missing geometry value
  produces an empty field.
- Any other column that merely happens to be named like a geometry but was not selected as
  *the* geometry column is uploaded as an ordinary column: it keeps its (normalized) name
  and its value is written verbatim, not re-encoded.

## Ordinary columns

- Non-geometry column names are normalized to SQL-safe names (lower-cased, spaces and other
  unsupported characters replaced, etc.) in both the `CREATE TABLE` and the `COPY` column
  list. Values are written in their string form; a null value produces an empty field.
- Column SQL types in `CREATE TABLE` are derived from the DataFrame dtypes:
  `float64`/`float32` → `numeric`, `int64` → `bigint`, `int32` → `integer`,
  `object` → `text`, `bool` → `boolean`, datetime dtypes → `timestamp`; anything else
  defaults to `text`.

## `with_lnglat`

- When `with_lnglat=(lng_col, lat_col)` is passed, an extra geometry column named
  `the_geom` of type `geometry(Point, 4326)` is appended after the regular columns, built
  per row as `SRID=4326;POINT (<lng> <lat>)`. The `lng_col` and `lat_col` columns are still
  uploaded as ordinary columns.
- When `with_lnglat` is used, any geometry column that would otherwise have been detected in
  the DataFrame is dropped, so the synthesized point is the only geometry uploaded.

## Statement format

The `COPY` statement keeps its existing shape:

```
COPY <table>(<col1>,<col2>,...) FROM stdin WITH (FORMAT csv, DELIMITER '|');
```

with the destination column names joined by commas (no spaces). Each streamed row is the
column values joined by `|` and terminated by a newline, encoded to bytes.
