behavior of || after if changes after formatting
## Metadata

- Ruby version: `ruby 2.7.2p137 (2020-10-01 revision 5445e04352) [x86_64-darwin20]`
- `prettier` gem version: `1.5.5`
- Options:
  - [x] `rubyHashLabel`
  - [x] `rubyModifier`
  - [x] `rubySingleQuote`
  - [ ] `rubyToProc`
  - [ ] `trailingComma`

## Input

```ruby
if condition
  original
end || fallback
```

## Current output

```ruby
original if condition || fallback
```

This is does not produce equivalent behavior; if `condition` is false, it will return `original` instead of `fallback`.

---

I'm agnostic on the correct output, but I think this is equivalent to the input:

```ruby
if condition
  original
else
  fallback
end
```
