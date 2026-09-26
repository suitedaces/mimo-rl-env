## Sync IDA Pro type definitions across collaborating analysts

We're using Polichombr to collaborate on reversing a sample with two
other analysts. The current server-side IDA actions cover most of what
we need — global names, comments, and structs all sync between our IDA
instances through the API — but there's one IDA action that doesn't get
shared: **type definitions** (the ones you set by hitting `Y` on a
variable, function, or address in IDA Pro).

### What we'd like to do

In IDA, I'll often refine a function prototype on a `sub_xxxxxx`, e.g.
turn the default `int __cdecl sub_401000(int, int)` into something
meaningful like `BOOL __stdcall ParseConfigBlob(char *blob, size_t
len)`. Then I want my teammates to pick that up automatically the next
time their plugin pulls from the server, the same way they pick up the
names and comments I made.

Right now, there's no way to do this through Polichombr. Names get
pushed and pulled fine, structs get pushed and pulled fine, but the
type info I set with `Y` just stays local in my `.idb` and the rest of
the team has to re-discover it independently. For functions with
non-trivial prototypes (lots of pointers, callbacks, custom typedefs)
this ends up being a real source of duplicated work.

### What we'd expect

Ideally the server should treat applied type definitions as just
another kind of IDA action, alongside names / comments / structs:

- the plugin should be able to push a type definition for a given
  sample at a given address,
- and a teammate's plugin should be able to query, for a given sample,
  the type definitions that have been recorded — with the same kind of
  filtering you already support for names and comments (by address, or
  only the ones added after a given timestamp, so we don't keep
  re-pulling the whole history on every sync).

Would it be possible to add this? Happy to test against any branch.

(For API shape, mirroring the existing `/samples/<sid>/names/` style would make sense — e.g. a `types`-flavored endpoint that accepts an `address` + `typedef` payload on push and returns the recorded `typedefs` on pull.)
