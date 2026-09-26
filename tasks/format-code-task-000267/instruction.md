Generation of schemaorg according to the specification
### Issue Summary

It all started with a discussion on the forum: https://forum.ghost.org/t/schema-org-generate/36772/7

Apparently, schemaorg is not being generated correctly at the moment.

Take, for example, a page https://ghost.org/changelog/vscode-extension/

Here's her json-id

```

<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",
    "publisher": {
       ...
    },
    "author": {
        ....
    },
    "headline": "Ghost VS Code extension",
    "url": "https://ghost.org/changelog/vscode-extension/",
    "datePublished": "2023-01-30T16:51:03.000Z",
    "dateModified": "2023-01-30T16:51:03.000Z",
    "image": {
        ...
    },
    "keywords": "New",
    "description": "....",
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://ghost.org/changelog/"
    }
}
</script>
```

mainEntityOfPage [according to the explanation of the developers schemaorg](https://github.com/schemaorg/schemaorg/discussions/3274) should contain a link to the article page, not a link to the blog.

### Steps to Reproduce

Run ghost :)

### Ghost Version

5.36+

### Node.js Version

-

### How did you install Ghost?

docker

### Database type

MySQL 8

### Browser & OS version

_No response_

### Relevant log / error output

_No response_

### Code of Conduct

- [X] I agree to be friendly and polite to people in this repository
