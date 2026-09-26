### `netutil.NewOneConnListener` API 有点乱，而且有几个小问题

在 `net/netutil` 里现在有两个几乎一样的构造函数：

```go
func NewOneConnListener(c net.Conn) net.Listener
func NewOneConnListenerFrom(c net.Conn, ln net.Listener) net.Listener
```

两者区别只是返回的 listener 在被问 `Addr()` 时给的是 dummy 地址，还是从
传进来的 `ln` 上借一个。调用点其实只在乎"给我一个一次性的 listener 把
这个已经握在手里的 `net.Conn` 喂给 `http.Server.Serve`"，并不真的需要
一个完整的 `net.Listener` 来做 Addr 来源 —— 它们想要的只是一个地址。
现在为了让 Addr 不是 dummy，调用方被迫先持有/构造一个 `net.Listener` 传
进来，挺别扭。

顺带看了下 `oneConnListener` 的实现还有两个小问题：

1. `Accept()` 直接读写 `l.conn` 字段没有任何同步。理论上 `http.Server`
   只 Accept 一次就完事，但这个类型暴露的是 `net.Listener` 接口，调用方
   或者底层框架并发调一下 Accept 完全是合法的，目前会 race。

2. `Close()` 没有专门实现，走的是嵌入的 `net.Listener.Close()`。在
   `NewOneConnListener(c)` 这条路径下嵌入的是 `dummyListener`，它的
   Close 是空操作；但语义上 Close 之后再 Accept 应该立刻拿到 EOF，
   现在不一定能保证（取决于内部 conn 字段当时的状态）。

希望这块整理一下：让构造函数的形态更简单，调用方想要自定义 Addr 时不必
凭空塞一个 listener 进来；同时 Accept / Close 的并发与终止语义把住。

现有调用点：

- `ipn/ipnserver/server.go` 里用 `NewOneConnListener` 包一个
  `protoSwitchConn` 喂给 `http.Server.Serve`，不关心 Addr。
- `ipn/ipnlocal/peerapi.go` 里用 `NewOneConnListenerFrom(c, pln.ln)`
  喂给 peerAPI 的 `http.Server.Serve`，想让 server 看到的 Addr 跟真正
  的 peerAPI listener 一致。

这两个用法理想情况下应该长得差不多，只是一个不在乎 Addr、一个在乎。
