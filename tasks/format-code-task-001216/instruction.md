support .gitignore and other git config files in reuse addheader
`reuse addheader .gitignore --copyright TEST --license "CC0-1.0"` now gives 

> reuse addheader: error: '.gitignore' does not have a recognised file extension, please use --style

See https://stackoverflow.com/questions/8865848/comments-in-gitignore

> Yes, you may put comments in there. They however must start at the beginning of a line.
