False positive in `consistent-function-scoping` when using `React.useEffect`
Since #588, `consistent-function-scoping` is not triggered for the following code:

```ts
import { useEffect } from "react";

useEffect(() => {
  function foo() {}
}, []);
```

This makes sense – see #392. However, when React is imported as a namespace, the same code is no longer valid:

```ts
import * as React from "react";

React.useEffect(() => {
  function foo() {} // Move function 'foo' to the outer scope. eslint(unicorn/consistent-function-scoping)
}, []);
```

Reporting React as a namespace [is OK](https://twitter.com/dan_abramov/status/1308739731551858689). I prefer this method because it produces smaller git diffs and prevents `no-unused-var` when refactoring.

Happy to submit a PR with the fix around next weekend. If anyone wants to create one earlier, please feel free to! 🙌

Relevant condition and its test:

https://github.com/sindresorhus/eslint-plugin-unicorn/blob/d9fd6642312537d8df5002e99022564bfea776bb/rules/consistent-function-scoping.js#L92-L97

https://github.com/sindresorhus/eslint-plugin-unicorn/blob/d9fd6642312537d8df5002e99022564bfea776bb/test/consistent-function-scoping.mjs#L266-L271
