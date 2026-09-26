## 希望 mgr 包能直接以编程方式拿到"解析后的数据"

我在给 logkit 写一些配置调试 / 自测工具，目标是在 Go 代码里直接验证一份 runner 配置（reader + parser 的组合）能不能跑通：先按 reader 配置读一条原始日志，再按 parser 配置解析它，看解析结果是不是符合预期。

`mgr.GetRawData(readerConfig)` 这一半已经够用了，传一份 reader 配置就能拿到一行 raw 数据，很方便。

但解析这一半就比较尴尬。整个 mgr 包里能把 "parser 配置 + 一段 sample log" 跑成 `[]Data` 的入口只有 `RestService.PostParse` 这个 HTTP handler，而且里面的逻辑全都 inline 写在 echo handler 闭包里 —— 按 parser type 拆 sample log、不同 type 各自的特殊处理、走 parser registry 实例化、最后调 `Parse` —— 想在非 HTTP 场景复用这套，要么真的起一个 web server 然后 POST 进去自己解响应，要么就把 handler 里那一整段抄一份到自己代码里，每次 parser 类型加新分支两边都得维护。

希望能有一个跟 `GetRawData` 对称的、mgr 包级别可以直接调用的函数：传一份 parser 配置（里面带 sample log），返回解析出来的 `[]Data`。这样写预览 / 测试 / 离线校验工具就不用抄那段 switch 了，`PostParse` 自己也可以基于它实现，避免一份逻辑两个地方维护。

另外有个相关的小痛点：现在如果 sample log 是空字符串，或者 parser 配置 + 数据组合下来实际一条都没解析出来，调用方拿到的就是个空切片 + nil error，调试时分不清是"配置真的是对的、只是这段 sample 不该有结果"还是"哪里悄悄出错了"。如果新加的这个函数在这种"0 条解析结果"的情况下能直接返回 error 把信息（包括是哪个 parser 出的问题）带出来，会省很多事。

顺便建议把这类"按配置取数据"的工具集中放在一起 —— 现在 `GetRawData` 跟 manager 主体逻辑挤在 `mgr.go` 里有点格格不入，跟新增的解析工具一起单独成一个文件会更清楚。

命名上跟 `GetRawData` 对称即可，比如可以叫 `GetParsedData`。
