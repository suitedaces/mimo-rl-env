Regular expression does not match multi-line string
Regular expression does not match multi-line string.

```console
$ goawk 'BEGIN{VAR="a\nb"; print match(VAR, /^a.*b$/)}'
0
$ goawk 'BEGIN{VAR="a\nb"; print match(VAR, /(?s)^a.*b$/)}'
1

$ gawk 'BEGIN{VAR="a\nb"; print match(VAR, /^a.*b$/)}'
1
$ mawk 'BEGIN{VAR="a\nb"; print match(VAR, /^a.*b$/)}'
1
```
