Regression: `/*!` is changed into `/* !`
**Prettier pr-5206**
[Playground link](https://deploy-preview-5206--prettier.netlify.com/playground/#N4Igxg9gdgLgprEAuEB6AVAQgDpQATp4CiAHjAE4CGY8AJngGbkQC2eAbgK5x6S1wAjSgGc4uAngAWMGAAdhSVKgDmASxiTOAgHSQWqLnABWwg91QCANhAGowDWgHYAzGABMzgBwA2bx+cALACMDgICztTezt5gAUIMngFwlJ4AnO5gqMLkmXqyqpZw5KiylOSixdIslgC0peVF2ibihAASACoAsgAyeAAKZRV4AEIAnngAUhCS+ABKcMKqyngAFMbTUNoQ5MoAlC14nRC0qgyqcPQC4xOc5Krj2CAA1pRQypQkj3gAWpSjMKJ2AcAPJ3NRQSiWXjHHhXYh3J54ACC5HYqlowmE0AANIcIAAvAqWSj9LSWVRgPDdCkIUQHaRyRSoIqqJ7aZJwbRQOAwLKqFiyQpVSz1Cp8gVCmDVUWNZr4dCoEDYkAQWQwVTQYTIUBlZgAdwG5FpyBAlHYEHRSpAAioYCePIAyqUwKo3sgKNxlcKAOqSdQLZ1wB209SqNEwUYmsCYq2uiowPpUZQsSjIBiQ0TKkwkYa2+0wB2UFhwanctMZuDKmXkE1CK7WKBW2R3WDe9EaZCeAAMVeYom9VFkJubCyK7DgVqNAEdOKojYnKMnU0h05ZMyBRCxVO7yJ6N67lIUAIqcCDwctrysgGCUARt2gdpBuZUUSgFA8AYVYKZNUGgE+VThRHaW8tRXCsAF8IKAA)
```sh
--parser babylon
```

**Input:**
```jsx
/*!
 * Extracted from vue codebase
 * https://github.com/vuejs/vue/blob/cfd73c2386623341fdbb3ac636c4baf84ea89c2c/src/compiler/parser/html-parser.js
 * HTML Parser By John Resig (ejohn.org)
 * Modified by Juriy "kangax" Zaytsev
 * Original code by Erik Arvidsson, Mozilla Public License
 * http://erik.eae.net/simplehtmlparser/simplehtmlparser.js
 */
```

**Output:**
```jsx
/* !
 * Extracted from vue codebase
 * https://github.com/vuejs/vue/blob/cfd73c2386623341fdbb3ac636c4baf84ea89c2c/src/compiler/parser/html-parser.js
 * HTML Parser By John Resig (ejohn.org)
 * Modified by Juriy "kangax" Zaytsev
 * Original code by Erik Arvidsson, Mozilla Public License
 * http://erik.eae.net/simplehtmlparser/simplehtmlparser.js
 */

```

**Expected behavior:**
Same as input, see https://stackoverflow.com/a/42132113.

Looks like the change from #5206, cc @j-f1
