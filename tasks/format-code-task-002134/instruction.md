## A few rough edges I keep hitting when writing huntflows

I've been using Kestrel against a stix-shifter data source and ran into a
handful of things that look like bugs / usability problems. Filing them
together since they all came up in the same session.

### 1. Single-quoted property names in a STIX path don't parse

In STIX, property keys that contain hyphens (typical for extension types)
have to be wrapped in single quotes inside an object path, e.g.

```
extensions.'windows-pebinary-ext'.machine_hex
file:hashes.'SHA-256'
```

These work fine inside the pattern body of a `GET ... WHERE [...]`, but
the moment I try to use the same path in `disp`, `sort`, `group` or
`join`, parsing blows up:

```
pes = GET file FROM stixshifter://my_src
      WHERE [file:hashes.'SHA-256' MATCHES '.+']
disp pes attr extensions.'windows-pebinary-ext'.machine_hex
```

→ `KestrelSyntaxError` complaining about the `'` character. Same thing
with

```
sort pes by extensions.'windows-pebinary-ext'.machine_hex
```

These are legal STIX object paths, so it's surprising that Kestrel
accepts them in one place and rejects them in another.

### 2. Syntax errors are hard to act on

When I do hit a syntax error (e.g. while iterating on a statement and
mistyping a keyword, or the issue above), the message I get is something
like:

```
[ERROR] KestrelSyntaxError: invalid character "'" at line 1 column 23. ...
```

It tells me *where* I went wrong but nothing about what the parser was
actually willing to accept at that position. For anyone who hasn't
memorized the grammar this means a lot of guess-and-retry. Could the
error mention what was expected at that spot? That would make
self-service debugging way easier.

### 3. Variable summary shows inflated related-entity counts

After running e.g. a `FIND` or a multi-entity `GET`, the per-variable
summary table prints a `#` column for each related entity type. The
numbers I see there look too high — bigger than the number of distinct
related entities that actually exist in the store when I query the
underlying tables directly. It looks like the same record can be
contributing more than once to that count. The reported number should
reflect distinct related entities.

---

The single-quote thing is the one really blocking me right now (I can't
sort/display by PE extension fields at all). The other two are quality
of life but they came up in the same hunt so figured I'd mention them
here. Happy to split into separate issues if preferred.
