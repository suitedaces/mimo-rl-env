tls config MinVersion panic
### Summary 
The gosec rule for tls config's `MinVersion` panic when the value is declared in another file. Note that this seems to be a different issue than https://github.com/securego/gosec/issues/721.

### Steps to reproduce the behavior
**boom/main.go**:
```golang
package main

import (
	"crypto/tls"
	"fmt"
)

func main() {
	cfg := tls.Config{
		MinVersion: MinVer,
	}
	fmt.Println("tls min version", cfg.MinVersion)
}
```

**boom/const.go**:
```golang
package main

import "crypto/tls"

const MinVer = tls.VersionTLS13
```

### gosec version
```
Version: v2.9.6
Git tag: v2.9.6
Build date: 2022-01-25
```

### Go version (output of 'go version')
`go version go1.17.6 linux/amd64`

### Operating system / Environment
`Linux ArchLinux 5.16.2-arch1-1 #1 SMP PREEMPT Thu, 20 Jan 2022 16:18:29 +0000 x86_64 GNU/Linux`
### Expected behavior
No panic, no error.

### Actual behavior
```
% ./gosec boom/...
[gosec] 2022/01/25 16:04:53 Including rules: default
[gosec] 2022/01/25 16:04:53 Excluding rules: default
[gosec] 2022/01/25 16:04:53 Import directory: /tmp/tmp.gUfP7ksi5C/gosec/boom
[gosec] 2022/01/25 16:04:53 Checking package: main
[gosec] 2022/01/25 16:04:53 Checking file: /tmp/tmp.gUfP7ksi5C/gosec/boom/const.go
[gosec] 2022/01/25 16:04:53 Checking file: /tmp/tmp.gUfP7ksi5C/gosec/boom/main.go
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x20 pc=0x6d0b7c]

goroutine 1 [running]:
github.com/securego/gosec/v2/rules.(*insecureConfigTLS).processTLSConfVal(0xc00013e500, 0xc000f23260, 0xc0001a8070)
	/tmp/tmp.gUfP7ksi5C/gosec/rules/tls.go:91 +0x25c
github.com/securego/gosec/v2/rules.(*insecureConfigTLS).Match(0xc00013e500, {0x7dbcb0, 0xc000e7ecc0}, 0xc0001a8070)
	/tmp/tmp.gUfP7ksi5C/gosec/rules/tls.go:183 +0x147
github.com/securego/gosec/v2.(*Analyzer).Visit(0xc0001f8ea0, {0x7dbcb0, 0xc000e7ecc0})
	/tmp/tmp.gUfP7ksi5C/gosec/analyzer.go:425 +0x838
go/ast.Walk({0x7d5fc0, 0xc0001f8ea0}, {0x7dbcb0, 0xc000e7ecc0})
	/usr/lib/go/src/go/ast/walk.go:50 +0x5f
go/ast.walkExprList({0x7d5fc0, 0xc0001f8ea0}, {0xc000f44670, 0x1, 0x0})
	/usr/lib/go/src/go/ast/walk.go:24 +0x87
go/ast.Walk({0x7d5fc0, 0xc0001f8ea0}, {0x7dba80, 0xc000e7ed00})
	/usr/lib/go/src/go/ast/walk.go:208 +0x12b2
go/ast.walkStmtList({0x7d5fc0, 0xc0001f8ea0}, {0xc000e917a0, 0x2, 0x0})
	/usr/lib/go/src/go/ast/walk.go:30 +0x87
go/ast.Walk({0x7d5fc0, 0xc0001f8ea0}, {0x7dbb70, 0xc000f23290})
	/usr/lib/go/src/go/ast/walk.go:225 +0xedf
go/ast.Walk({0x7d5fc0, 0xc0001f8ea0}, {0x7dbe40, 0xc000f232c0})
	/usr/lib/go/src/go/ast/walk.go:346 +0x7dc
go/ast.walkDeclList({0x7d5fc0, 0xc0001f8ea0}, {0xc000e917c0, 0x2, 0x40ce14})
	/usr/lib/go/src/go/ast/walk.go:36 +0x87
go/ast.Walk({0x7d5fc0, 0xc0001f8ea0}, {0x7dbdf0, 0xc000f2d580})
	/usr/lib/go/src/go/ast/walk.go:355 +0x15c5
github.com/securego/gosec/v2.(*Analyzer).Check(0xc0001f8ea0, 0xc00041cdc0)
	/tmp/tmp.gUfP7ksi5C/gosec/analyzer.go:249 +0x565
github.com/securego/gosec/v2.(*Analyzer).Process(0xc0001f8ea0, {0x0, 0xc00010d010, 0xc00010d040}, {0xc00010d050, 0x1, 0x3d})
	/tmp/tmp.gUfP7ksi5C/gosec/analyzer.go:167 +0x1b7
main.main()
	/tmp/tmp.gUfP7ksi5C/gosec/cmd/gosec/main.go:395 +0x9b8
```
