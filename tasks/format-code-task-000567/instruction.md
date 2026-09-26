## Templater 在迭代 map / 嵌套 map 时缺少几个常用判断

我在用 `bin-templater` 渲染 `.cfg` 模板，数据源是 map（有时候是嵌套 map）。在模板里 `range` 一个 map 时碰到两类问题，现有的 `isMap` / `isArray` / `isString` 这套帮不上忙：

**1. 没法判断当前迭代到的 key 是 map 里的第一个还是最后一个**

典型场景是渲染逗号分隔列表，最后一项后面不能有逗号；或者第一项前面不加分隔符。模板里 `range` 一个 map 拿到 `$k, $v`，想做这种边界判断时，没有可以直接调用的函数。Go 原生 `text/template` 又没有 `last` 这种 helper，只能在外面把数据先转成 slice，但这对模板用户很不友好——而且需要一个跟模板里实际迭代顺序（按 key 排序）一致的"边界"判断，否则首尾认错了。

**2. 嵌套 map 里没法知道某个 value 处在第几层**

我有形如 `map[string]interface{}` 嵌套若干层的数据，渲染时想按层做缩进或者根据深度切换格式。当前模板里完全没有获取"某个 element 在这个嵌套 map 里的深度"的途径。

希望模板函数表里能补上这几类查询，让用户在模板里直接调用就行，不用把数据预先在 Go 代码里铺平。

I'd expect the new template helpers to be named something like `IsMapFirst` / `IsMapLast` / `HowDeep`, each taking the map plus the element being checked (e.g. `IsMapFirst $data $key`, `HowDeep $data $value`).
