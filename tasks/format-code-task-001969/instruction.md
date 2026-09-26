## Browser sniffing helpers should be deprecated by default; expose the UA parser for general use

I'm using MooTools and ran into two related awkward bits around `Browser`:

### 1. The default build still encourages UA sniffing

The `Browser` docs already say things like "use feature detection / progressive enhancement instead", and link to MDN's "Browser detection using the user agent" article warning people off sniffing. But the default (non-compat) build still sets all the things that *are* primarily used for sniffing:

```js
if (Browser.ie) { /* legacy hack */ }
if (Browser.firefox24) { /* ... */ }
if (Browser.Platform.mac) { /* ... */ }
```

These boolean aliases (`Browser.ie`, `Browser.firefox`, `Browser.chrome`, ..., and the `Browser.Platform.<name>` flags) basically only exist so people can branch on them — which is exactly what the docs tell us not to do. It feels inconsistent that the library ships them in the standard build while telling users not to use them. Could these be moved to the 1.4-compat build only, the same way `Browser.Engine` / `Browser.Plugins` already are, so a fresh project doesn't pick them up by default?

The genuinely useful, *informational* parts — knowing what name/version/platform we appear to be running on, e.g. for analytics or a debug overlay — should obviously still be reachable in the default build.

### 2. The UA parser is hidden / not usable for arbitrary strings

MooTools clearly has a working UA parser internally (it has to, to populate `Browser.name` etc.), but it only runs once at load time against `navigator.userAgent`. I'd like to use the same logic on other strings — for example, when I'm processing UA strings from server access logs to build a "browsers used by our visitors" chart, or just when I want to test parser behaviour for a specific UA in a unit test.

Right now there's no documented public way to do this: I either have to read into `Source/Browser/Browser.js` and call an undocumented internal, or reimplement the regex myself.

It would be great if the parser were a documented public API on `Browser` that I can call with any UA string (and ideally also accept a separate platform string, since a raw UA alone can't always tell you whether it's Mac vs Windows vs Linux), and have it hand back a structured result with the same fields the library itself reports.

So roughly, the ask is:

- default build no longer sets the sniffing-style aliases (`Browser.ie`, `Browser.firefox`…, plus the `Browser.Platform` boolean flags) — they live in the compat build for people who still need them;
- informational properties about the current browser/version/platform stay accessible in the default build;
- the UA-parsing function is promoted to a documented public API usable on arbitrary strings.

The public entry point I'd expect is something like `Browser.parseUA(uaString, platformString)`.
