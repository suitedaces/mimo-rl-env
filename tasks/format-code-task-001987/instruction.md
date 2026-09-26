## `get_es()` doesn't let callers override settings; `ES_DUMP_CURL` also seems to do nothing

I'm using elasticutils inside a Django project and `get_es()` is normally fine, but I keep running into two situations where it gets in my way.

**1. No way to ask for a one-off ES with different settings.**

For most request handlers the cached, shared `ES` is what I want, so `get_es()` returning the same thread-local instance is great. But sometimes I want a *different* one — for example, I have a management command that does bulk indexing and the default timeout from `settings.ES_TIMEOUT` is way too short for it; I'd like to use a longer timeout just for that script without changing the global setting (which would affect every request).

Today `get_es()` takes no arguments, so the only escape hatch I can find is to import `pyes` directly and construct an `ES(...)` myself. But then I'm bypassing all the elasticutils glue — `ES_HOSTS`, the default index from `ES_INDEXES`, the port-range check for thrift, etc. — and I have to copy that logic into my script. It would be a lot nicer if `get_es()` itself accepted overrides for the kinds of things I'd otherwise be passing to `pyes.ES`, while still falling back to my Django settings for everything I don't override.

It's also fine (preferred, even) if calling it with no arguments keeps the current "share one ES per thread" behavior — I only want to opt out of the cache when I'm explicitly asking for something custom.

**2. `ES_DUMP_CURL` doesn't actually print anything.**

The debugging docs suggest setting `ES_DUMP_CURL` to an object with a `write()` method to dump the curl commands elasticutils sends to ES. I tried it more or less verbatim:

```python
# settings.py
class CurlDumper(object):
    def write(self, s):
        print s

ES_DUMP_CURL = CurlDumper()
```

Then in a view I do `es = get_es()` and run a query through `S(...)`. I expected to see curl commands showing up in my runserver output, but nothing is printed — the dumper's `write` is never called. Queries themselves work fine, so it's not that ES is broken, it's that `dump_curl` doesn't seem to be wired through to the actual `ES` instance that `get_es()` hands back.

This is on `pyes` 0.15 (which the docs say is the recommended version). Whatever's going on, I'd expect that if I configure `ES_DUMP_CURL` and then use `get_es()`, the resulting `ES` actually dumps curl. Bonus: it would be great to be able to turn dumping on for just one call site (e.g. via the override mechanism from #1) without having to flip a global setting.
