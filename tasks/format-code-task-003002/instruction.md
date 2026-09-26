### Astro Info

```block
Astro                    v4.1.2
Node                     v20.9.0
System                   Windows (x64)
Package Manager          unknown
Output                   static
Adapter                  none
```


### If this issue only occurs in one browser, which browser is a problem?

_No response_

### Describe the Bug

Seems intentional but when strings with `&` are used in a meta head tag, they're encoded as `&#38;` during development and build which affects URLs with a query string with multiple search params e.g. an `og:image` link pointing to an API that dynamically generates the image with a title and description.

```html
<meta  
  name="og:image"  
  content={'https://example.com/api/og?title=hello&description=somedescription'}  
/>

<!-- <meta name="og:image" content="https://example.com/api/og?title=hello&#38;description=somedescription"> --> 
<!-- title=hello -->
```

For the Stackblitz example, when built, it is transformed into `&#38;` .

### What's the expected result?

Not escaped in this case?

```html
<meta  
  name="og:image"  
  content={'https://example.com/api/og?title=hello&description=somedescription'}  
/>

<!-- <meta name="og:image" content="https://example.com/api/og?title=hello&description=somedescription"> --> 
<!-- title=hello description=somedescription -->
```

### Link to Minimal Reproducible Example

https://stackblitz.com/edit/github-2f3s26?file=src%2Flayouts%2FLayout.astro

### Participation

- [X] I am willing to submit a pull request for this issue.
