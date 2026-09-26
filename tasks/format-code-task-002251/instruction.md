# Backed enums lose their backing type after PDepend's AST cache round-trip

When I run PDepend on a project that contains PHP 8.1 enums, the analysis results are not stable across runs — once the AST cache is involved, the same enum doesn't look the same as it did on the original parse.

Reproducer — a simple backed enum:

```php
<?php

enum HttpStatus: int
{
    case Ok = 200;
    case NotFound = 404;
}
```

**Fresh run** (no cache): PDepend correctly identifies this as a backed enum. `isBacked()` returns `true` and `getType()` returns the `int` scalar type.

**Second run** (cached AST is restored from disk): the *exact same file* now comes back looking like a basic, non-backed enum. `isBacked()` returns `false` and `getType()` returns `null`. Nothing in the source has changed between the two runs.

I'd expect an enum that goes through the cache to come back semantically identical to the freshly-parsed version — same backing type, same `isBacked()` result.
