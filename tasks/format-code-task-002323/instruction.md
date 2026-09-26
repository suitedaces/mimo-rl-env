YAML: Incorrect quotes are used when string contains mixed quotes
**Prettier 1.14.2**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEAdEByAhq3IBG6qUIANCBAA4wCW0AzsqFgE4sQDuACqwoylgBuEGgBMyBFljABrODADKlaTSgBzZDBYBXOOVX04LGFylqAtlmQAzLABtD5AFb0AHgCEps+Qqzm4ADKqcDb2jiDKLIYsyCAAnn52EpQsqjAA6mIwABbIABwADOQpEIbpUpSxKXDRgiHkLHAAjto0jaZYFlZItg56IIbmNJo6-fSqanZwAIraEPChfeQwWPiZojnIAEzLUjR2EwDCEOaWsVDQ9SDahgAqq-y9hgC+z0A)
```sh
--parser yaml
```

**Input:**
```yaml
"'a\"b"

```

**Output:**
```yaml
''a"b'

```

**Second Output:**
```yaml
SyntaxError: Document is not valid YAML (bad indentation?) (1:3)
> 1 | ''a"b'
    |   ^^^
> 2 | 
    | ^
```
