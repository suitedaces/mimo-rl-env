[Bug]: import JSON fails when coverage is enabled
### Version

29.4.3

### Steps to reproduce

data.json
```json
{"hello":"world"}
```
jest.config.json
```json
{
    "testEnvironment": "node",
    "transform": {}
}
```
package.json
```json
{
  "name": "jest_json_coverage",
  "scripts": {
    "test": "node --experimental-json-modules --experimental-vm-modules node_modules/jest/bin/jest.js"
  },
  "type": "module",
  "devDependencies": { "jest": "29.4.3" }
}
```
example.test.js
```js
import myJSON from './data.json' assert {type:"json"};
test("t00",()=>{console.log(myJSON);})
```
**Commands:**
```sh
$ npm t  # works ok
$ npm t -- --coverage # fails
```


### Expected behavior

Test passes without runtime error.

### Actual behavior

output:
```sh
  ● Test suite failed to run

    Jest encountered an unexpected token
    Jest failed to parse a file. This happens e.g. when your code or its dependencies use non-standard JavaScript syntax, or when Jest is not configured to support such syntax.

    Out of the box Jest supports Babel, which will be used to transform your files into valid JS based on your Babel configuration.

    By default "node_modules" folder is ignored by transformers.

    Here's what you can do:
     • If you are trying to use ECMAScript Modules, see https://jestjs.io/docs/ecmascript-modules for how to enable it.
     • If you are trying to use TypeScript, see https://jestjs.io/docs/getting-started#using-typescript
     • To have some of your "node_modules" files transformed, you can specify a custom "transformIgnorePatterns" in your config.
     • If you need a custom transformation specify a "transform" option in your config.
     • If you simply want to mock your non-JS modules (e.g. binary assets) you can stub them out with the "moduleNameMapper" config option.

    You'll find more details and examples of these config options in the docs:
    https://jestjs.io/docs/configuration
    For information about custom transformations, see:
    https://jestjs.io/docs/code-transformation

    Details:

    SyntaxError: /home/armfazh/tmp/jest_json_coverage/data.json: Missing semicolon. (1:8)

    > 1 | {"hello":"world"}
        |         ^
      2 |

      at instantiate (node_modules/@babel/parser/src/parse-error/credentials.ts:62:21)
      at instantiate (node_modules/@babel/parser/src/parse-error.ts:60:12)
      at Parser.toParseError [as raise] (node_modules/@babel/parser/src/tokenizer/index.ts:1464:19)
      at Parser.raise [as semicolon] (node_modules/@babel/parser/src/parser/util.ts:138:10)
      at Parser.semicolon [as parseExpressionStatement] (node_modules/@babel/parser/src/parser/statement.ts:1282:10)
      at Parser.parseExpressionStatement [as parseStatementContent] (node_modules/@babel/parser/src/parser/statement.ts:643:19)
      at Parser.parseStatementContent [as parseStatementLike] (node_modules/@babel/parser/src/parser/statement.ts:416:17)
      at Parser.parseStatementLike [as parseStatementListItem] (node_modules/@babel/parser/src/parser/statement.ts:365:17)
      at Parser.parseStatementListItem [as parseBlockOrModuleBlockBody] (node_modules/@babel/parser/src/parser/statement.ts:1363:16)
      at Parser.parseBlockOrModuleBlockBody [as parseBlockBody] (node_modules/@babel/parser/src/parser/statement.ts:1336:10)
      at Parser.parseBlockBody [as parseBlock] (node_modules/@babel/parser/src/parser/statement.ts:1304:10)
      at Parser.parseBlock [as parseStatementContent] (node_modules/@babel/parser/src/parser/statement.ts:547:21)
      at Parser.parseStatementContent [as parseStatementLike] (node_modules/@babel/parser/src/parser/statement.ts:416:17)
      at Parser.parseStatementLike [as parseModuleItem] (node_modules/@babel/parser/src/parser/statement.ts:353:17)
      at Parser.parseModuleItem [as parseBlockOrModuleBlockBody] (node_modules/@babel/parser/src/parser/statement.ts:1362:16)
      at Parser.parseBlockOrModuleBlockBody [as parseBlockBody] (node_modules/@babel/parser/src/parser/statement.ts:1336:10)
      at Parser.parseBlockBody [as parseProgram] (node_modules/@babel/parser/src/parser/statement.ts:226:10)
      at Parser.parseProgram [as parseTopLevel] (node_modules/@babel/parser/src/parser/statement.ts:208:25)
      at Parser.parseTopLevel [as parse] (node_modules/@babel/parser/src/parser/index.ts:45:10)
      at parse (node_modules/@babel/parser/src/index.ts:67:38)
      at parser (node_modules/@babel/core/src/parser/index.ts:28:19)
          at parser.next (<anonymous>)
      at normalizeFile (node_modules/@babel/core/src/transformation/normalize-file.ts:51:24)
          at normalizeFile.next (<anonymous>)
      at run (node_modules/@babel/core/src/transformation/index.ts:38:36)
          at run.next (<anonymous>)
      at transform (node_modules/@babel/core/src/transform.ts:29:20)
          at transform.next (<anonymous>)
      at evaluateSync (node_modules/gensync/index.js:251:28)
      at sync (node_modules/gensync/index.js:89:14)
      at fn (node_modules/@babel/core/src/errors/rewrite-stack-trace.ts:97:14)
      at transformSync (node_modules/@babel/core/src/transform.ts:66:52)
      at ScriptTransformer._instrumentFile (node_modules/@jest/transform/build/ScriptTransformer.js:389:46)
      at ScriptTransformer._buildTransformResult (node_modules/@jest/transform/build/ScriptTransformer.js:491:33)
      at ScriptTransformer.transformSourceAsync (node_modules/@jest/transform/build/ScriptTransformer.js:605:17)
      at ScriptTransformer._transformAndBuildScriptAsync (node_modules/@jest/transform/build/ScriptTransformer.js:636:35)
      at ScriptTransformer.transformAsync (node_modules/@jest/transform/build/ScriptTransformer.js:700:14)
          at async Promise.all (index 0)

```

### Additional context

_No response_

### Environment

```shell
System:
    OS: Linux 5.4 Ubuntu 20.04.5 LTS (Focal Fossa)
    CPU: (8) x64 Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz
  Binaries:
    Node: 18.0.0 - ~/.nvm/versions/node/v18.0.0/bin/node
    npm: 8.7.0 - ~/.nvm/versions/node/v18.0.0/bin/npm
  npmPackages:
    jest: 29.4.3 => 29.4.3
```
