adding secret with colon in name fails
### Summary
A secret name with a colon is interpreted as a K/V pair, instead of a secret name.

### Steps To Reproduce
```bash
 ~$ gopass insert test:test

Error: Usage: gopass insert name
```

### Expected behavior
If only  a single element is specified, then it should be taken as the secret name, even if it successfully parses as a K/V pair.

### Environment
<!--
Please complete the following information (see note below)
-->

- OS: Fedora 32
- gopass Version: gopass 1.9.2+e2d1549f452a0df1fc52e42e7d0f654334d7144e (e2d1549f452a0df1fc52e42e7d0f654334d7144e) go1.14.2 linux amd64

<!--
**PLEASE NOTE**

There is a package named gopass in the official Debian repository.
This package is not related to this project in any way. If you
installed gopass from the Debian archives report any bugs in
the Debian BTS.
-->

### Additional context
Causes problems with using gopass as the backend for the lastest version of `aws-vault`, which stores the OIDC token as `gopass insert -f -m oidc:<hostname>`
