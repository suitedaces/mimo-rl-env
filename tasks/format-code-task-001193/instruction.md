## `history.push` / `history.replace` 类型不接受 location 对象

history v4 的 API 允许我用两种方式调用 `push` 和 `replace`：传一个 path 字符串（加可选 state），或者直接传一个 location 对象，例如：

```js
import createBrowserHistory from 'history/createBrowserHistory';

const history = createBrowserHistory();

// 形式 1：path + state（这种 flow 不报错）
history.push('/foo', { from: 'bar' });

// 形式 2：location 对象（这种 flow 报错）
history.push({
  pathname: '/foo',
  search: '?x=1',
  hash: '#section',
});
```

第二种调用是 history 库官方文档里推荐的用法（在需要同时指定 pathname/search/hash 时很常见，react-router 内部也是这么用的），运行时完全正常，但当前 flow-typed 里 `BrowserHistory` / `MemoryHistory` / `HashHistory` 的 `push` 和 `replace` 签名只覆盖了 `(path: string, state?)`，所以传 location 对象时 flow 直接报类型错误。

`replace` 也有同样的问题。

另外顺带：`BrowserLocation` 和 `MemoryLocation` 里 `state` 的类型是 `string`，但实际上 state 是用户自己塞进去的任意对象（react-router 文档里的例子也是对象），写成 string 太窄了，传 `{ from: '/login' }` 这种就过不了类型检查。

希望这些类型能同时支持 path-字符串和 location-对象两种调用形式。
