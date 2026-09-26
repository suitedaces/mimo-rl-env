## Feature request: iterate over a numeric range from a template

I'd like to be able to loop over a numeric range directly inside a jet template. Typical use cases are rendering pagination links, repeating a UI element N times, or emitting a numbered list.

Right now I don't see a way to do this from the template side alone. What I end up doing is building a throwaway slice in Go just so the template has something to `range` over:

```go
// in the handler
nums := make([]int, 10)
for i := range nums {
    nums[i] = i
}
vars.Set("nums", nums)
```

```
{{ range i := nums }}
    <a href="?page={{ i }}">{{ i }}</a>
{{ end }}
```

This feels backwards — the template is the side that knows it wants to render "page 1 through page N", but it can't express that without Go-side glue. Every place that needs a numeric loop ends up repeating the same boilerplate, and it leaks template concerns into handler code.

Other template engines provide something for this out of the box (Python's `range`, Twig's `..` operator, etc.). Could jet have an equivalent builtin so a template can produce a numeric sequence on its own, without the caller having to prepare a slice for it? I'd expect something like `ints(from, to)` usable directly in a `range`.
