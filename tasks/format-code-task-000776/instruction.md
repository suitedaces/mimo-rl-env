## Feature request: fallback / conditional transforms for summary string templates

I'm using summary string templates with filter syntax to format entry summaries. Right now I can use `upper`, `lower` and `date('<format>')`, which is great, but I keep running into two cases that aren't covered.

### 1. Fallback when a field is empty

Some entries in my collection don't have every field filled in. For example, I have an optional `subtitle` field, and when it's missing my summary ends up with a dangling separator or an empty section:

```yaml
collections:
  - name: 'posts'
    label: 'Posts'
    folder: '_posts'
    summary: "{{title}} — {{subtitle}}"
    fields:
      - { label: 'Title', name: 'title', widget: 'string' }
      - { label: 'Subtitle', name: 'subtitle', widget: 'string', required: false }
```

I'd like a way, from within the template syntax, to say "if this field is empty, use this literal string instead" — so I can write something like `{{subtitle | <fallback to 'Untitled'>}}` and get `Untitled` when the field is blank, without having to write a custom preview/summary component just for that.

### 2. Pick one of two values based on whether a field is set

Related, but slightly different: sometimes I don't want to print the field's value at all, I just want to branch on whether it's truthy and emit one string or another. E.g. a `featured` boolean controlling whether the summary shows `★` or nothing, or a `draft` flag controlling whether to show `(draft)` or `(published)`.

Today the only way I can do this is by post-processing the summary outside of the CMS config, which defeats the point of having the filter syntax.

Could the template filter pipeline be extended to cover these two cases? They feel like a natural extension of the existing `upper` / `lower` / `date(...)` filters and would remove a lot of awkwardness around optional / boolean fields in summary strings.

Naming-wise I'd expect something like `default('...')` for case 1 and `ternary('...', '...')` for case 2, to match the existing filter call style.
