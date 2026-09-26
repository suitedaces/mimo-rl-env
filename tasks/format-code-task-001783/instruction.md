## Inconsistent target ID attribute makes mission-agnostic code awkward

I'm writing a few small helper scripts that work with light curves and pixel files from different missions (Kepler, K2, TESS) interchangeably — things like logging, summarising a batch run, or just printing which object I'm currently processing.

The thing that keeps tripping me up is that the target identifier is named differently depending on which mission produced the data:

- `KeplerLightCurve` / `KeplerLightCurveFile` / Kepler `TargetPixelFile` expose it as `keplerid`
- `TessLightCurve` / `TessLightCurveFile` / TESS `TargetPixelFile` expose it as `ticid`

So whenever I want to do something as simple as "print the ID of this target", I end up writing branches like:

```python
def describe(obj):
    if isinstance(obj, (KeplerLightCurve, KeplerLightCurveFile)):
        ident = obj.keplerid
    elif isinstance(obj, (TessLightCurve, TessLightCurveFile)):
        ident = obj.ticid
    else:
        ident = None
    print("Processing target", ident)
```

every time I touch a new object type, in every script. It also means downstream tools (plotting helpers, table builders, anything that takes "a light curve" as input) can't just look up the target's identifier without first knowing which mission the data came from.

Would it be possible to expose a single, mission-agnostic attribute on these objects that returns the underlying identifier? On a Kepler/K2 object it would give back the same value as `keplerid`, and on a TESS object it would give back the same value as `ticid`. Ideally the same convention would apply to `LightCurve`, `LightCurveFile`, and `TargetPixelFile` so I can write the helper above without any `isinstance` checks at all. The existing `keplerid` / `ticid` attributes should keep working as they do today.

A name like `targetid` would feel natural for this generic attribute, if that helps.
