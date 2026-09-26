### GeneratePayload / GetABI RPC 在 seelejs 里没法用

我在用 seelejs（JS 的 RPC 客户端）调 seele 节点，想走这套流程发合约调用：

1. 先用 `GetABI` 通过合约地址把 abi 拿回来
2. 再把 abi + method name + 参数喂给 `GeneratePayload` 拿到 payload，发交易

但这两个 RPC 在 JS 端基本没法串起来：

- `GetABI` 返回的是 Go 这边的 `abi.ABI` 结构体，通过 JSON-RPC 出来是一坨嵌套对象，JS 这边没办法直接拿去喂下一步——seelejs 拿到的也不是当初写到链上的那个 abi 字符串。

- `GeneratePayload` 第一个参数声明的就是 `abi.ABI` 这个 Go 结构体，JS 客户端根本没法构造一个匹配的对象传过去。就算 `GetABI` 的返回能原样传回来，签名也对不上。

- 即使硬绕过去把 payload 算出来，`GeneratePayload` 返回的是 `[]byte`，JSON-RPC 序列化出来是 base64，而后续发交易的 RPC 想要的是 `0x...` 十六进制字符串，又得在 JS 那头再转一道。

总的来说这两个 API 当前的入参/返回类型是按 Go 内部使用设计的，从 JSON-RPC 客户端（尤其是 seelejs）的角度完全用不起来。希望能把这两个 RPC 调整成在 JSON-RPC 上自然可用的形式，让 JS 客户端可以直接：拿 abi → 调 GeneratePayload(abi, method, args...) → 得到能直接塞进交易的 payload。
