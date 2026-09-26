[en] Descendant template inline qualifiers in the wrong place
In <https://kaikki.org/dictionary/Proto-Finnic/meaning/v/ve/veci.html>, a descendant line like

`{{desc|liv|ve’ž|vez<q:Salaca>}}`

becomes

```json
{
  "lang": "Livonian",
  "lang_code": "liv",
  "tags": [
    "Salaca"
  ],
  "word": "ve’ž"
},
{
  "lang": "Livonian",
  "lang_code": "liv",
  "word": "vez"
}
```

In reality, the tag should apply to `vez`, not to `ve’ž`.
