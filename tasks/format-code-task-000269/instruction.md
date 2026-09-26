Footnote reference links are plaintext in post excerpts
## Issue Summary

Footnote reference links (which landed in #4270) in posts are shown in post excerpts as plain text
## Steps to Reproduce
- Add a footnote in the first few words of a post `Lorem ipsum dolor [^1]`
- Save/publish post
- Go to a page on the blog that shows excerpts (index, for example)
- See the footnote reference in plain text `Lorem ipsum dolor 1`

These references need to be stripped from excerpts
