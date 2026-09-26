## 用 SetQuery 传 map 时，value 为空字符串的字段会被默认丢掉

最近用 gout 对接一个老的第三方搜索接口，参数比较多，大概是这样：

```go
query := gout.H{
    "t":          1296,
    "callback":   "searchresult",
    "q":          "美食",
    "stype":      1,
    "pagesize":   100,
    "pagenum":    1,
    "imageType":  2,
    "imageColor": "",
    "brand":      "",
    "imageSType": "",
    "fr":         1,
    "sortFlag":   1,
    "imageUType": "",
    "btype":      "",
    "authid":     "",
    "_":          1611822443760,
}

gout.GET(url).Debug(true).SetQuery(query).Do()
```

打开 Debug 看实际发出去的请求，URL 上只剩下非空 value 的那几个 key，所有 value 是 `""` 的字段（`imageColor` / `brand` / `imageSType` / `imageUType` / `btype` / `authid`）全都被丢掉了。对方接口要求这些字段必须出现在请求里（哪怕 value 为空），不然校验直接挂掉。

从调用者视角看，我把一个 key 显式塞进 `gout.H{}`，就是想让它出现在请求里。空字符串也是一种有效的值，跟"完全不写这个 key"是两个语义。lib 主动帮我"清理"反而是种意外行为——同事第一次看到也以为是自己代码写错了，翻了半天 issue 才知道是默认会过滤。

`SetHeader` 似乎也是同样的处理方式。

希望调整一下默认行为，让传入的空字符串字段也能正常出现在最终请求里，让"我写啥就发啥"成为默认表现，而不是反过来需要额外配置才能拿到。
