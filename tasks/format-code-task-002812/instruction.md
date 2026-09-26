## `EventTimeSource` 的 `NewTimer` 在 `Reset` 之后会送出旧时间

我在写单元测试时用 `clock.NewEventTimeSource()` 做 fake clock，通过 `NewTimer` 拿到 `(<-chan time.Time, Timer)` 来模拟一个会触发的定时器。我想在同一个 timer 上 fire 两次：先让它 fire 一次、读出时间、验证；然后 `Reset` 一个新的 duration，再 advance 时间让它第二次 fire，从 channel 里读出第二次的时间。

期望行为是跟标准库 `time.NewTimer` 一致——每次 timer fire 时，channel 上送的应该是这一次 fire 时刻的当前时间。但用 fake clock 时，第二次从 channel 收到的时间和第一次完全一样，是 timer 最初创建时算出来的那个 deadline，而不是 `Reset` 之后应该的新 deadline。

大致复现思路：

```go
ts := clock.NewEventTimeSource()
ch, timer := ts.NewTimer(1 * time.Second)

ts.Advance(1 * time.Second)
firstFire := <-ch  // OK, 是初始 deadline

timer.Reset(2 * time.Second)
ts.Advance(2 * time.Second)
secondFire := <-ch  // 期望: 现在的当前时间; 实际: 还是 firstFire
```

stdlib 里 `time.Timer` Reset 之后再次 fire，channel 上拿到的就是新一次触发时的当前时间，fake clock 这边应该匹配同样的语义，否则用 fake clock 模拟"周期性触发"或"重试退避"这类逻辑的测试会拿到错误的时间戳。
