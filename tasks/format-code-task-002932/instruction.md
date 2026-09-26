### 描述

我在用 `var-bottom-navigation` 配合 `fixed` 让导航栏固定在页面底部，类似下面这样：

```html
<template>
  <div class="page">
    <!-- 一些很长的内容 -->
    <p v-for="i in 50" :key="i">第 {{ i }} 行内容</p>

    <var-bottom-navigation fixed v-model:active="active">
      <var-bottom-navigation-item label="首页" icon="home" />
      <var-bottom-navigation-item label="搜索" icon="magnify" />
      <var-bottom-navigation-item label="收藏" icon="heart" />
      <var-bottom-navigation-item label="我的" icon="account-circle" />
    </var-bottom-navigation>
  </div>
</template>
```

因为 `fixed` 让导航栏脱离了文档流，页面内容滚动到最底部时，最后一段内容会被这个固定的导航栏直接盖住，看不到了。

目前要解决这个问题，只能在外层自己手动加一个和导航栏同高的空 `div`，或者给最外层加一个 `padding-bottom`，但导航栏的实际高度可能受 `variant`、`safe-area` 等属性、以及是否有 `fab` 影响（带 fab 的时候 fab 凸出在导航栏上方，遮挡范围更大），手动估算高度并不稳定。

### 期望

希望 `var-bottom-navigation` 自己能提供一个开关，在 `fixed` 启用时自动在底部放一个等高的占位元素，把内容顶上去，让最后的内容不会被遮挡，也希望这个行为在带 fab 的场景下能正确处理 fab 的额外高度。其它一些类似的底部固定组件（比如 tabbar）一般也有类似的占位选项，希望这里也支持一下。

新开关名我倾向叫 `placeholder` 这种简短的 boolean prop。
