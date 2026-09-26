jest-runtime, jest-transform: share cacheFS between runtime and transformer
<!-- Love Jest? Please consider supporting our collective: 👉  https://opencollective.com/jest/donate -->

## 🚀 Feature Proposal

<!-- A clear and concise description of what the feature is. -->
Currently, when `ts-jest`/`jest-preset-angular` performs code compilation + type checking with TypeScript LanguageService/Program, TypeScript will attempt to do module resolution itself to gather enough information for the process.

The problem is when doing module resolution, TypeScript will also perform `fs.readFileSync` to get file content. So we end up in the situation that some files which are already read by TypeScript will be read again by Jest, which causes extra I/O on disk. 

Therefore, I'd like to propose a feature request that `jest-runtime` shares `cacheFS` with `jest-transform`. The idea is that custom transformer can get/set this `cacheFS` so that already-read files shouldn't be read again.

The prototype implementation is: `jest-runtime` passes `cacheFS` to `ScriptTransformer`, `ScriptTransformer` passes that `cacheFS` to `process`.


## Motivation

<!-- Please outline the motivation for the proposal. -->
Improve performance by reducing I/O.

## Example

<!-- Please provide an example for how this feature would be used. -->
This will help `ts-jest`/`jest-preset-angular` to speed up test run with `isolatedModules: false`

## Pitch

The implementation will require changes in `jest-runtime` and `jest-transform` so it is core of Jest.

cc @thymikee @SimenB
