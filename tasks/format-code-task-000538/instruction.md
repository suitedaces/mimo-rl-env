Is a template is must in v1.6?

I use c.Ctx.Output.Body() direct write reponse , it works  in beego v1.5 . 

```
c.Ctx.Output.Header("Content-Type", "application/xml; charset=utf-8")
c.Ctx.Output.Body(response)
```

But wrong in beego v1.6

```
2016/02/09 21:50:55 [router.go:854][C] Handler crashed with error can't find templatefile in the path:maincontroller/get.tpl 
2016/02/09 21:50:55 [router.go:860][C] /usr/local/go/src/runtime/asm_amd64.s:437 
2016/02/09 21:50:55 [router.go:860][C] /usr/local/go/src/runtime/panic.go:423 
2016/02/09 21:50:55 [router.go:860][C] /Users/brian/dev/go/src/github.com/astaxie/beego/controller.go:262 
2016/02/09 21:50:55 [router.go:860][C] /Users/brian/dev/go/src/github.com/astaxie/beego/controller.go:183 
2016/02/09 21:50:55 [router.go:860][C] /Users/brian/dev/go/src/github.com/astaxie/beego/router.go:784 
2016/02/09 21:50:55 [router.go:860][C] /usr/local/go/src/net/http/server.go:1862 
2016/02/09 21:50:55 [router.go:860][C] /usr/local/go/src/net/http/server.go:1361 
2016/02/09 21:50:55 [router.go:860][C] /usr/local/go/src/runtime/asm_amd64.s:1721 
```
