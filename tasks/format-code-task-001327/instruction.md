## AsciiDoc TableOfContents is broken when headings contain inline formatting

I'm using Hugo with the `asciidocext` content format (Asciidoctor installed) and rendering `{{ .TableOfContents }}` in my single page template. Most of my headings work fine, but as soon as a heading contains inline formatting — usually inline code with backticks — the TOC comes out wrong.

### Reproduction

Content file `content/posts/example.adoc`:

```asciidoc
---
title: "Example"
---
:toc: macro
:toclevels: 4

toc::[]

== Introduction

Some intro text.

== Using `make` to build

Stuff about make.

== Working with `git`

Stuff about git.
```

Template just outputs `{{ .TableOfContents }}` in an `<aside>`.

### What I see

The rendered TOC has the wrong number of entries — way more `<li>` elements than the three `==` headings I wrote — and the parts wrapped in backticks (`make`, `git`) are nowhere to be found. The entries that do appear contain only the surrounding text fragments like `Using ` and ` to build` as separate items, which makes the navigation list look completely scrambled.

If I rewrite the headings without any inline formatting (plain words only), the TOC comes out correctly with exactly three entries. So it only goes wrong when a heading mixes plain text with an inline element.

### What I expected

The TOC should have one entry per `==` heading regardless of whether the heading contains inline `code`, `*emphasis*`, etc., and the inline formatting in the heading should be preserved in the TOC link text the same way Asciidoctor itself renders it in the body.
