## Setting values at a nested path — `GetPath` has no write-side equivalent

I'm using simplejson to manipulate some nested JSON (a config blob, in my case). Reading deep into it is really clean with `GetPath`:

```go
host := js.GetPath("server", "database", "host").MustString()
```

But when I want to **update** a value at a nested location, I can't find a clean way to do it. `Set` only operates on the top-level map, so to change something a few levels down I end up doing the type-assertion dance manually:

```go
m, _ := js.Map()
inner, _ := m["server"].(map[string]interface{})
db, _ := inner["database"].(map[string]interface{})
db["host"] = "newhost"
```

…and that's only the happy path — if any of the intermediate keys aren't there yet (e.g. I'm building the structure up from an empty `New()`), I also have to check for each one and create the missing maps myself before I can descend further. It gets ugly fast and there's no way it's the intended API.

Could we get a write-side counterpart to `GetPath`? Something where I hand it the path and the value and it lands the value at the leaf, taking care of creating any intermediate structure that doesn't exist yet. The symmetry with `GetPath` would make the API a lot more usable for anything beyond flat objects.

The new method I'd expect is something like `SetPath(branch, val)`, mirroring `GetPath`. Handing it an empty path could just replace the whole root value.
