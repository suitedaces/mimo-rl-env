## Detail view renders YAML lists and nested dicts incorrectly

I store some entries in gopass that have YAML structure beyond simple key/value, e.g. a list of recovery codes plus a few nested dictionaries. Something like:

```yaml
a_long_random_password
---
url: www.github.com
email: abc@gmail.com

recovery codes:
- abcde-12345
- fghij-67890
- zyxwv-05432
- test1:
  - alksdfj
  - alksdfjalsf
  - ["bla", "blub"]
  - test2:
    - alksd
    - aklsdjf
- last code here!
dict:
 dict1:
  dict1.1: 1.1
  dict1.2: 1.2
 dict2:
  dict2.1:
    dict2.1.1: one
    dict2.1.2: two
 dict3: 0
```

When I open the detail view for this entry in the popup, the rendering of `recovery codes` and `dict` is wrong:

- For the list items under `recovery codes`, each plain string item (e.g. `abcde-12345`) is rendered with a stray label in front of it like `undefined:` or `null:`. Lists don't have keys for their items, so there shouldn't be a label there at all.
- The nesting is visually flat. Items several levels deep (e.g. things inside `test1` → `test2`, or `dict.dict1.dict1.1`) don't get any visible indentation, so the structure is unreadable — you can't tell what belongs to what.
- It looks broken in both Chrome and Firefox, and the two browsers don't even render it the same way.

Top-level flat fields like `url:` and `email:` look fine — the problem only shows up once the value is a list or a nested object.

I'd expect the detail view to display nested structures with their hierarchy visible, and list items to render as items (no fake key prefix).
