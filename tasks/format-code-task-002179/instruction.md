## `| default ""` does not work on CDS variables in pipeline scripts

I'm writing a step script in a CDS pipeline and I want to use a CDS application variable that may or may not be defined. According to the [variables doc](docs/content/workflows/pipelines/variables.md), `default` is listed as one of the available helpers, so I tried using it with an empty string as the fallback:

```bash
echo "value={{.cds.app.foo | default \"\"}}"
```

My expectation: if `cds.app.foo` is not defined (or is empty), the rendered script should be

```
value=
```

and if it is defined, I get its value.

What actually happens: the `| default ""` part is not honored — the placeholder doesn't get replaced with an empty string the way I'd expect. Passing a non-empty fallback like `| default "something"` behaves differently from passing `""`, but `""` is a perfectly reasonable thing to want here (I literally want the variable to disappear from the output if it's not set).

It would be great if `{{.cds.app.xxx | default ""}}` worked the same way as `{{.cds.app.xxx | default "someValue"}}` — empty string is just another default value.

While we're at it, the helpers section of the variables doc only lists `default` by name without an example; an example showing both `| default ""` and `| default "defaultValue"` would make the intended usage much clearer (same for `upper`, which is mentioned in the intro example but not shown in the helpers list).
