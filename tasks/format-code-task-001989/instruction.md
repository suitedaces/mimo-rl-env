Parsing issue with semi-colons in :before and :after content
Reported by a user of the KA HTML/CSS environment, which uses slowparse.

Before/After Pseudoelements can't have semicolons in their content because the error checker mistakes the semicolon for the end of the CSS rule and concludes that the closing quote is a property name with no value set.

This code works:

```
h1::before{content:'&lt'} /* Inserts "&lt" before every header */
```

but this code, with a semicolon inside the quotes, does not work:

```
h1::before{content:'&lt;'} /* Inserts an opening angle bracket ("&lt;") before every header */
```

I replicated on Thimble here: https://thimble.webmaker.org/project/110284/remix
