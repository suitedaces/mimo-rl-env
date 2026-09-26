# Problem Statement

我在项目里用 @mlvis/manifold，遇到几个挺烦的事想问下能不能一起处理下：一个是装这个包必须额外装 antd 才不报 peer dep warning，但我们项目本身根本没用 antd，能不能不要强制依赖它？另外我想 dispatch 那个更新 base columns 的 action，从包里 import `updateBaseCols` 一直拿到 undefined，这个能修一下吗？还有就是 feature-list-view 的 chart 我喂进去的数据里有 Date 类型的值，控制台一直刷 PropTypes 的 warning，说 Date 不在允许的类型里，但其实渲染是正常的，能让它把 Date 也认成合法值么？

# Expected outcomes

- Package dependency behavior:
  - Installing or consuming `@mlvis/manifold` should not require consumers to install `antd` solely to satisfy `@mlvis/manifold` peer dependencies.
  - `@mlvis/manifold` should not require the separate `@mlvis/segment-filters` package for its filter UI behavior.
- Public action API:
  - `updateBaseCols` should be importable from the manifold action exports and should be a usable action creator for updating base columns.
- Feature list chart prop validation:
  - Feature-list-view chart data should accept `Date` values in the same data positions where primitive chart values are accepted, without emitting a React prop validation warning for those `Date` values.

# Implementation notes

- The exact internal organization of UI/filter components, helper functions, and state handling is up to the implementation, as long as the public package/API behavior above is satisfied.
- Dependency changes should be made at the package boundary where they affect consumers; avoid requiring downstream users to install libraries they do not use directly.
- Existing valid chart value types should continue to be accepted while adding support for `Date` values.
