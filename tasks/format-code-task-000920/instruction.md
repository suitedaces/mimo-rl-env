我这边有些 RN/Fabric 的封装场景只能拿到原生组件的 ref/handle，不太方便走组件实例上的 `setNativeProps`。能不能在 `ReactNative` / `ReactFabric` 顶层也暴露一个 `setNativeProps` 入口，让我可以直接对这个 native ref 做命令式 props 更新？如果不小心传了非 native component 的 ref，最好能给个 warning 就别继续更新了。

Expected outcomes:
- `ReactNative.setNativeProps` and `ReactFabric.setNativeProps` are available as top-level APIs for imperatively applying valid native props to the native view represented by a native component ref or handle.
- Calling either top-level API with a ref that does not represent a native component emits a developer warning that explains the ref is not a native component and stops without performing a native view update.
- Calling either top-level API with props that produce no native update does not perform a native view update.

Implementation notes:
- The exact sharing strategy between the React Native and Fabric renderers is up to the implementation.
- The validation location, update payload construction, and no-op detection mechanism are implementation details, as long as the public behavior above is preserved.
