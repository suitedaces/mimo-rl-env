Bug: @typescript-eslint/prefer-nullish-coalescing mal-fixes nested condition
### Before You File a Bug Report Please Confirm You Have Done The Following...

- [x] I have tried restarting my IDE and the issue persists.
- [x] I have updated to the latest version of the packages.
- [x] I have [searched for related issues](https://github.com/typescript-eslint/typescript-eslint/issues?q=is%3Aissue+label%3A%22package%3A+eslint-plugin%22) and found none that matched my issue.
- [x] I have [read the FAQ](https://typescript-eslint.io/linting/troubleshooting) and my problem is not listed.

### Playground Link

https://typescript-eslint.io/play/#ts=5.7.2&showAST=types&fileType=.tsx&code=DYUwLgBAhgXBDOYBOBLAdgcwgHwgVzQBMQAzdEQgKFEgCM4BvCAWxHnigxDkVUwgC%2BOfEVLkqAYwD2aRBEgBeCAAowPZOgwBKCAoB88ypWmzIJKVN3RKEW3YD81u3bi0bzhxFoA6Vu04g7h4QcGDKAEQYwFK0UMDeIEhIUkjeBADWaFIA7mjhWpRAA&eslintrc=N4KABGBEBOCuA2BTAzpAXGUEKQAIBcBPABxQGNoBLY-AWhXkoDt8B6Y6RAM0WlqYSNkAC1pkA9gEMkyMswDm6KL2jjokcGAC%2BILUA&tsconfig=N4KABGBEDGD2C2AHAlgGwKYCcDyiAuysAdgM6QBcYoEEkJemy0eAcgK6qoDCAFutAGsylBm3TgwAXxCSgA&tokens=false

### Repro Code

```TypeScript
let a: string | undefined
let b: { message: string } | undefined
const t = (t: string) => t

const foo = a
      ? a
      : b
        ? b.message
        : t("global.error.unknown")

```

The error happens when running the `Fix` on this rule: It breaks the code.

### ESLint Config

```javascript
module.exports = {
  parser: "@typescript-eslint/parser",
  rules: {
    "@typescript-eslint/prefer-nullish-coalescing": "error",
  },
};
```

### tsconfig

```jsonc
{
  "compilerOptions": {
    "strictNullChecks": true
  }
}
```

### Expected Result

```ts
let a: string | undefined
let b: { message: string } | undefined
const t = (t: string) => t

const foo = a ?? (b
        ? b.message
        : t("global.error.unknown"))

```

### Actual Result

```ts
let a: string | undefined
let b: { message: string } | undefined
const t = (t: string) => t

const foo = a ?? b
        ? b.message
        : t("global.error.unknown")
```

### Additional Info

_No response_
