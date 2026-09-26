# Fix page merging into writer pages and add layer control

Merging a page into a page that belongs to a `PdfWriter` is currently broken.
A typical "stamp / n-up" workflow like:

```python
writer = PdfWriter()
page = writer.add_blank_page(width, height)
page.merge_page(reader.pages[0])
writer.write("out.pdf")
```

produces a **blank** output page: the merged content and its resources (fonts,
images, graphics states, …) are lost once the document is written out and read
back. The merged content is only visible while everything stays in memory.

Make merging work end to end when the target page lives in a `PdfWriter`: after
`writer.write(...)` and re-reading the produced PDF, the merged page must still
contain the content (and the resources it depends on) coming from the page that
was merged in. In other words, merging a reader page into a writer page and then
writing the document must not yield a blank/white page.

Additionally, expose a public method `merge_transformed_page(page2, ctm, over=True,
expand=False)` on a page that merges `page2` after applying a transformation
matrix. `ctm` may be either a 6-element transformation tuple or a
`Transformation` instance. This method is a regular, supported method — calling
it must **not** raise a deprecation error.

Both merging paths must support an `over` flag controlling the stacking order of
the merged content:

- `over=True` (the default) layers `page2` **on top of** the existing page —
  `page2`'s content is drawn after the current page's content.
- `over=False` layers `page2` **underneath** the existing page — `page2`'s
  content is drawn before the current page's content.

The flag must take effect for content merged into writer pages and survive the
write + re-read round trip.
