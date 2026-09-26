An asterisk in a @forward statement triggers scss/operator-no-unspaced
See the prefix docs for `@forward`: https://sass-lang.com/documentation/at-rules/forward#adding-a-prefix:

```scss
@forward "src/list" as list-*;
```

> Content: Expected single space after "*" (scss/operator-no-unspaced)
