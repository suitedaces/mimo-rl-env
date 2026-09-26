## Confusing `PermissionError` from `Fido.fetch` when `path` contains directories that don't exist yet

I'm downloading some AIA data with `Fido` and I want it organised into a tidy local folder structure, e.g.

```python
from sunpy.net import Fido, attrs as a

results = Fido.search(a.Time('2012/3/4', '2012/3/5'), a.Instrument('AIA'))
files = Fido.fetch(results, path='/home/me/solar_data/aia/2012/03/')
```

`/home/me/solar_data/` exists, but I haven't pre-created the `aia/2012/03/` part yet — I was expecting `Fido.fetch` to create the missing subdirectories for me (or at least to tell me clearly if I have to make them myself).

Instead I immediately get:

```
PermissionError: You do not have permission to write file in this directory
```

Two things make this really frustrating:

1. **It isn't actually a permission problem.** I own `/home/me/solar_data/` and can write to it just fine (`touch /home/me/solar_data/x` works). The "no permission" wording sent me off chasing `chmod` / ownership issues for a while before I realised the real reason the check was failing was just that the deeper path didn't exist yet.

2. **The message doesn't tell me which directory it's complaining about.** In my real script I'm building `path` from several template fields and looping over multiple queries, so when this fires I have no idea which path triggered it. I have to add my own `print(path)` before every `Fido.fetch` call just to find out.

Could the error message at least include the directory that was actually checked? And ideally, if I pass a `path` whose leaf doesn't exist yet, the writability check should be done against the nearest existing parent directory rather than reporting a misleading permission error for a path that simply isn't there.
