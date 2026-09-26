dollar-variable-first-in-block - ignore @use
I think `"ignore": ["imports"]` option should also ignore `@use`.

Real-world example:

```scss
@use "sass:color";

$primary-color: #f26e21 !default;
$secondary-color: color.change($primary-color, $alpha: 0.08) !default;
```

Actual: `Expected $-variable to be first in block (scss/dollar-variable-first-in-block)`

Expected: no warnings
