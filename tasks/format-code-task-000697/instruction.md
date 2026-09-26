## `Lines.Bytes()` doesn't include a trailing newline

I'm embedding the texteditor widget in my app to let users edit source
files. To save changes I grab the buffer contents with `Lines.Bytes()`
and write the result to disk.

The saved files never end with a newline character, even though
everything else in the editor is preserved byte-for-byte. This causes
`git` to flag "No newline at end of file" on every save, and a few
command-line tools (wc, some linters/formatters) complain similarly.

By convention text files end with a newline (per POSIX). Could
`Lines.Bytes()` return the content with a final `\n` so the output is
suitable for writing straight to a `.go`/`.txt`/etc. file without any
post-processing on my end?
