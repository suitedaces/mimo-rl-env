I want a `blueprint_book` command-line tool for packing and unpacking Factorio blueprint books from newline-delimited blueprint strings on standard input. It should be installed as the `blueprint_book` console command and invoked as `blueprint_book pack [--label LABEL]` or `blueprint_book unpack`.

For `blueprint_book pack`, the command should read blueprint strings from stdin until EOF, decode each one, put them into a Factorio `blueprint_book` object with `item` set to `blueprint-book`, `active_index` set to `0`, and version `281474976710656`, assign each contained blueprint an `index` starting at 0 in input order, and print one encoded blueprint-book string on stdout. If `--label Pair` is supplied, the encoded book should include the book label `Pair`. For example, packing these two input lines with `blueprint_book pack --label Pair`:

`0eNqrVkrKKU0tKMrMK1GyUqhWyixJzQUykER1FJTKUouKM/PzgOJGFoYm5iaW5mbmhgZmpmZAuZzEpNQckI78vFSl2loADV8YQw==`
`0eNqrVkrKKU0tKMrMK1GyUqhWyixJzQUykER1FJTKUouKM/PzgOJGFoYm5iaW5mbmhgZmpmZAuZzEpNQckI6S8nyl2loADdIYWw==`

should print this single line and exit 0:

`0eNqrVkrKKU0tKMrMK4lPys/PVrJSqFbKLEnNBTIQUrpgKR0FpcTkksyy1PjMvJTUCqAKA6BQWWpRcWZ+HpBnZGFoYm5iaW5mbmhgZmoGlMtJTErNAZkUkJhZBNIPN7EYKBpdjeBjt1eJWPPz81KVaoECcIcBOdQzvaQ8H8V0w9rY2loAVG5fsw==`

For `blueprint_book unpack`, the command should read one encoded blueprint-book string from stdin, decode its `blueprint_book.blueprints` list, and print each contained blueprint as its own encoded blueprint string on stdout in book order. Given the packed example above on stdin, `blueprint_book unpack` should print the two original blueprint strings as two output lines and exit 0. Invalid modes should be rejected by the CLI parser with a non-zero exit code and a usage/error message on stderr; `blueprint_book --help` should print usage describing the `pack` and `unpack` modes plus the `--label` option and exit 0.
