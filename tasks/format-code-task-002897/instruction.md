Bug: [no-deprecated] doesn't report usage of a deprecated private identifier
### Before You File a Bug Report Please Confirm You Have Done The Following...

- [x] I have tried restarting my IDE and the issue persists.
- [x] I have updated to the latest version of the packages.
- [x] I have [searched for related issues](https://github.com/typescript-eslint/typescript-eslint/issues?q=is%3Aissue+label%3A%22package%3A+eslint-plugin%22) and found none that matched my issue.
- [x] I have [read the FAQ](https://typescript-eslint.io/linting/troubleshooting) and my problem is not listed.

### Playground Link

https://typescript-eslint.io/play/#ts=5.3.3&fileType=.ts&code=MYGwhgzhAEAq0G8BQ1oHoBUHoAEAmApgA4BOBwYALgXtBmitAMQBmA9m9ALzQAUAlNwB8iRqjRpoAOhmMAvgG4kjAEZgSA0anGSIACzYBXELTJE2JStBWGreNgQgA7AOSUx0SnoCWEKaw4BJVQ5JFCgA&eslintrc=N4KABGBEBOCuA2BTAzpAXGUEKQAIBcBPABxQGNoBLY-AWhXkoDt8B6Jge1oBNFjpEZAIb5E3dGADakRNGgdokALrgwAXxBqgA&tsconfig=N4KABGBEDGD2C2AHAlgGwKYCcDyiAuysAdgM6QBcYoEEkJemy0eAcgK6qoDCAFutAGsylBm3TgwAXxCSgA&tokens=false

### Repro Code

```TypeScript
class T {
  /** @deprecated */
  #foo = () => {
    // ...
  };

  bar() {
    // should report but doesn't
    this.#foo();
  }
}
```

### ESLint Config

```javascript
module.exports = {
  parser: "@typescript-eslint/parser",
  rules: {
    "@typescript-eslint/no-deprecated": ["error"],
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

I expected the rule to report this, since TypeScript also shows this as deprecated.

### Actual Result

This wasn't reported by the rule.

### Additional Info

_No response_
