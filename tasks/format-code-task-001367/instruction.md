logging: log.Entry.Severity can't unmarshal after marshalling
**Client**
logging

**Environment**
MacOS Mojave

**Go Environment**
```
go version go1.15.5 darwin/amd64
GOARCH="amd64"
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOPROXY="https://proxy.golang.org,direct"
GOROOT="/usr/local/Cellar/go/1.15.5/libexec"
GOSUMDB="sum.golang.org"
GOTOOLDIR="/usr/local/Cellar/go/1.15.5/libexec/pkg/tool/darwin_amd64"
GCCGO="gccgo"
AR="ar"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
GOMOD=""
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/__/kst87n5n6xs1wr9vn3gw9xxh0000gn/T/go-build111216510=/tmp/go-build -gno-record-gcc-switches -fno-common"
```
**Code**
```go
package main

import (
	"fmt"
	"encoding/json"
	"cloud.google.com/go/logging"
)

func main() {
	entry := logging.Entry { Payload: "test log", Severity: logging.Info}
	j, err := json.Marshal(entry)
	if err != nil {
		panic(err)
	}

	var entryU logging.Entry
	err = json.Unmarshal(j, &entryU)
	if err != nil {
		panic(err)
	}
}
```

**Expected behavior**
Marshaling then Unmarshalling a logging.Entry struct should produce the same struct without errors.

**Actual behavior**
Unmarshalling has an error
```
panic: json: cannot unmarshal number into Go struct field Entry.Severity of type string
```

This is due to `logging.Entry.Severity` having an `UnmarshalJSON` method that only parses `string` `Severity` but during Marshaling, `Severity` is written as a number since it's underlying type is `int`


**Additional context**
This occurred while I was trying to process logs from `logging/logadmin` that had been saved as JSON, assuming Marshalling/Unmarshalling would be symmetrical.
