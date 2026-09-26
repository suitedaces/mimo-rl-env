## Multi-line repeated keys in Org mode front matter aren't recognized as arrays (except for a hard-coded few)

I'm using `.org` files as content in my Hugo site and writing front matter in Org mode style. Org documents commonly let you set an array-valued keyword by repeating the same `#+KEY:` line, e.g.

```org
#+TITLE: Hello world
#+AUTHORS: Alice
#+AUTHORS: Bob
#+AUTHORS: Carol
#+DATE: 2024-01-01
```

In my template I then do something like

```go-html-template
{{ range .Params.authors }}
  <span>{{ . }}</span>
{{ end }}
```

…and nothing renders. If I dump the value with `{{ printf "%#v" .Params.authors }}` I can see that `authors` came in as a single string with the names mashed together, not as a list of three entries. So `range` has nothing to iterate over.

What's odd is that the exact same multi-line style *does* produce a list — but only for a few specific keys. If I use `#+TAGS:`, `#+CATEGORIES:` or `#+ALIASES:` repeated across lines, I get a proper array in `.Params`. Every other key I try comes back as one merged string. On top of that, when I do use one of those three keys this way, Hugo logs a deprecation warning at me, which suggests this auto-conversion path is something you're trying to move away from anyway.

The documented escape hatch is `#+KEY[]: VALUE_1 VALUE_2` (whitespace-separated on one line), and that does work for arbitrary keys. But:

- It forces everything onto one line, which is awkward when individual values contain spaces or when there are many of them.
- It's not how people normally write multi-valued keywords in Org — the natural Org convention is to just repeat the keyword line, and that convention should work for *any* key, not only the three Hugo happens to special-case.

Could the Org front matter parser treat a repeated `#+KEY:` (i.e. a keyword whose accumulated value spans multiple lines) as an array for any key, the same way it already does for tags/categories/aliases — and drop the deprecation-warning special case while it's at it? That way the example above would give me `.Params.authors` as a real list I can `range` over, and the docs for the Org front matter format would match what users actually write.
