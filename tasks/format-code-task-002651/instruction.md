Imports may get removed if using Prettier range-start/range-end options
**Steps to reproduce**
- Create a trivial project with a few files:

`package.json:`
```
{
  "devDependencies": {
    "prettier": "3.0.3",
    "prettier-plugin-organize-imports": "3.2.3"
  }
}
```
`.prettierrc:`
```
{
  "plugins": [
    "prettier-plugin-organize-imports"
  ]
}
```
`foo.ts:`
```
export const foo = 0;
```
`bar.ts:`
```
import {foo} from "./foo";

let bar = foo;
```

- Run `prettier --range-end=27 bar.ts`. (In fact, any range end between 1 and 30 will demonstrate the bug)

**Expected result**
- No changes in file

**Actual result**
- Import statement disappears:
```


let bar = foo;
```

The problem is crucial for WebStrom and other JetBrains IDEs because Prettier integration in JetBrains IDEs ask Prettier to format only the imports block pretty often.
