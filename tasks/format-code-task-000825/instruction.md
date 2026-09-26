# Add AsciiDoc input support

Docling can already ingest a handful of "declarative" formats (HTML, Word, PowerPoint) — formats
that can be turned straight into a `DoclingDocument` without running a recognition pipeline. We want
to add **AsciiDoc** as a first-class input format alongside those.

## What to build

Teach the library to recognise AsciiDoc and convert it. Concretely:

1. **Register the format.** Add a new member `ASCIIDOC` (value `"asciidoc"`) to the input-format
   enumeration, and wire it into the library's format metadata so AsciiDoc is associated with the
   file extensions `asciidoc` and `adoc` and with the media type `text/asciidoc` (the media-type →
   format lookup must resolve `text/asciidoc` back to the new format).

2. **Provide a backend.** Expose a declarative document backend `AsciiDocBackend` importable from
   `docling.backend.asciidoc_backend`. It must follow the same backend interface as the other
   declarative backends:
   - it is constructed from an `InputDocument` and a path or `BytesIO` stream, reading the source as
     UTF-8 text;
   - `is_valid()` returns whether the source was read successfully;
   - `supports_pagination()` returns `False`;
   - `supported_formats()` returns exactly the set containing the new AsciiDoc format;
   - `convert()` parses the source and returns a `DoclingDocument`.

## Parsing contract

`convert()` walks the document line by line and builds the `DoclingDocument` in reading order:

- **Document title** — a line beginning with `= ` (a single `=` followed by a space). Its remaining
  text becomes a text item labelled as a title.
- **Section headings** — a line beginning with two or more `=` followed by whitespace. The number of
  `=` characters determines the nesting: `==` is a heading of level 1, `===` level 2, and so on (the
  heading level is the count of `=` minus one). The remaining text is the heading text.
- **List items** — lines beginning (optionally indented) with `*`, `-`, or a number followed by `.`
  (e.g. `1.`), followed by a space. Consecutive list items are collected into a list group, and each
  becomes a list item carrying the item's text (without the marker).
- **Tables** — a block delimited by lines equal to `|===`. Each row line looks like
  `| a | b | c`; cells are the `|`-separated, whitespace-trimmed, non-empty segments. The resulting
  table reports its row count and column count (columns = the widest row), and each parsed cell text
  is placed at its row/column position.
- **Images** — a line beginning with `image::` produces a picture item.
- **Paragraphs** — runs of consecutive non-empty lines that match none of the above are buffered and,
  on the next blank line (or at end of input), emitted as a single paragraph text item whose text is
  the buffered lines joined by single spaces.

The backend should accept both a filesystem `Path` and an in-memory `BytesIO` stream as its source.
