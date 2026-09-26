## XLIFF: ASCII control characters don't survive a round-trip

I'm using `translate.storage.xliff` to manage some translation units whose
source text contains ASCII control characters (in my case BEL `\x07`, but
I expect the same for the other unprintable control codes). Writing seems
fine, but reading the same file back gives me back something different
from what I put in.

Minimal repro:

```python
from translate.storage import xliff

store = xliff.xlifffile()
unit = store.addsourceunit(u"hello\x07world")
unit.target = u"bonjour\x07monde"

data = bytes(store)
# print(data) shows the control char has been replaced by something like &#x7;
# which is fine — it's not legal as a raw XML character.

store2 = xliff.xlifffile.parsestring(data)
u = store2.units[0]
print(repr(u.source))   # I expected u'hello\x07world'
print(repr(u.target))   # I expected u'bonjour\x07monde'
```

What I actually get back from `u.source` / `u.target` is the literal
escaped string (the `&#x...;` form), not the original control character.
So whatever the storage does on the way out isn't being reversed on the
way in, and the unit I read is no longer equal to the unit I wrote.

It would be nice if setting a value and then parsing the serialized file
gave me the original text back for these control characters.
