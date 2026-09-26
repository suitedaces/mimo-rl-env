## Feature request: kebab-case transform for tag values

I'm using `gomodifytags` to add `json` tags to my structs, but the API I'm targeting expects field names in kebab-case (lowercase words separated by hyphens), e.g. a field `MyExample` should serialize as `"my-example"`.

Right now `-transform` only supports `snakecase` and `camelcase`:

```
$ gomodifytags -file foo.go -line 4,6 -add-tags json -transform snakecase
```
gives me `json:"my_example"`, and `camelcase` gives me `json:"myExample"`. There's no option to get `json:"my-example"`.

It would be great if `-transform` supported a hyphen-separated lowercase style as well, so that:

```go
type foo struct {
    bar       string
    MyExample bool
    MyAnother []string
}
```

could be rewritten to:

```go
type foo struct {
    bar       string   `json:"bar"`
    MyExample bool     `json:"my-example"`
    MyAnother []string `json:"my-another"`
}

```

without having to manually fix up every tag after running the tool.

A name like `lispcase` for the new `-transform` value would be fine.
