## In-memory test registry doesn't support listing tags

I'm using `pkg/registry` to spin up a local fake registry in my integration tests (via `registry.New()`), which is great for exercising push/pull flows without a real backend. The problem is that the code I'm trying to test also lists tags for a repo — i.e. it hits `GET /v2/<name>/tags/list`, which is part of the distribution spec.

Roughly what my test does:

```go
s := httptest.NewServer(registry.New())
defer s.Close()

u, _ := url.Parse(s.URL)
repo, _ := name.NewRepository(u.Host + "/foo/bar")

// push a couple of tagged images here using remote.Write ...

tags, err := remote.List(repo)
// expect to get back the tags I just pushed
```

After pushing a few tags to the fake registry, the call that lists tags doesn't come back with them — the endpoint isn't handled by the registry at all, so I can't use this package to test any code path that lists tags for a repository.

It'd be great if the in-process registry implemented `GET /v2/<name>/tags/list` per the distribution spec, so that code which lists tags against it works the same way it does against a real registry.
