我在把一部分 Firebase web modular database 代码迁到 `@react-native-firebase/database`，现在 `off` 和 `enableLogging` 这两个 import 直接就找不到，TS 也过不了。能不能先让 modular 入口也暴露这两个 API，哪怕 native 这边暂时只是提示不支持，也别让我卡在导入和类型检查这里。

Expected outcomes:
- `enableLogging` is available as a named import from the modular `@react-native-firebase/database` entrypoint, and TypeScript accepts its Firebase Web modular-compatible call forms.
- Calling `enableLogging` at runtime does not silently succeed; it reports native non-support by throwing an error whose message is `enableLogging() is not implemented`.
- `off` is available as a named import from the modular `@react-native-firebase/database` entrypoint, and TypeScript accepts its Firebase Web modular-compatible call forms.
- Calling `off` at runtime does not silently succeed; it reports native non-support by throwing an error whose message is `off() is not implemented`.

Implementation notes:
- Keep the behavior aligned with the package’s existing modular API conventions, but the specific file organization and internal implementation details are up to the implementer.
- These APIs are compatibility stubs for the native implementation, not full native listener/logging implementations.
