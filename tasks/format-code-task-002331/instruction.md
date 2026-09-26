**Prettier 2.0.5**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuE8DOMA6UAEOD8OA9AFQ6QC2FCWueeJR29OAZhBMzkjgEYCGAJwDc2bOlp5CpchCo0u9fjkaK2HLjwEjsIADQgIABxgBLaGmSghgiAHcACkISWU-ADZ3+AT0sHegvxgANZwMADKRkGmUADmyDCCAK5wBgAWMBTuAOpppuhRYHDhLvmmAG753sjgaH4gMWhwgjAOgbEU-MisHk0GAFZoAB4AQoEhYeH81AAyMXDdvakgg0PhMbHucACKSRDwi+59IFGCTYI1MN5GcGhggqYm+icPsNmmACYwacgAHAAMBiMtia2UCRhqwNuzXKCwMAEc9vA2sZXCB+GgALRQOBwD5456COCI0xEtr8DpdJA9I7LJoUUwJZJ0jZbXb7BbUpYGGD8XjvL4-JAAJh5gVM7g2AGE5J0arcAKzPJJNAAqfNcNOO5RSAEkoPjYOF7o8YABBA3hK5bQ5NAC+dqAA)
```sh
--parser babel
```

**Input:**
```tsx
test
  ? /* comment
     */
    foo
  : bar;

test
  ? /* comment
     a */
    foo
  : bar;

```

**Output:**
```tsx
test
  ? /* comment
     */
    foo
  : bar;

test ? /* comment
     a */ foo : bar;

```

**Expected behavior:**
```tsx
test
  ? /* comment
     */
    foo
  : bar;

test
  ? /* comment
     a */
    foo
  : bar;

```
