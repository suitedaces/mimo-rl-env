Rule `nested-structs` errors on an interface func "set" return value
**Describe the bug**
When the `nested-structs` rule is enabled, any interfaces with a function returning a Go "set" using an empty struct `struct{}` as the value causes a linting error.

**To Reproduce**
Steps to reproduce the behavior:

Create the following Go source file:
```go
// sample.go

package main

type mySetInterface interface {
   GetSet() map[string]struct{}
}

var _ mySetInterface

type empty struct{}

type myTypedSetInterface interface {
   GetSet() map[string]empty
}

var _ myTypedSetInterface

type mySetStruct struct{}

func (mySetStruct) GetSet() map[string]struct{} {
   return map[string]struct{}{}
}

var _ mySetStruct
```

Create the following configuration file:

```toml
# config.toml

confidence = 0.8
enableAllRules = false
severity = "error"
errorCode = 1
warningCode = 1

[rule.nested-structs]
  disabled = false
```

Run revive with the configuration file on that given file / package:
`go run github.com/mgechev/revive@v1.2.4 -config config.toml .`

**Expected behavior**
No error occurs for returning / using a standard Go "Set", or include a config switch to disable this on the `nested-structs` rule.

**Logs**
```
sample.go:4:22: no nested structs are allowed
exit status 1
```

**Desktop:**

OS: `macOS 13.1`
Version of Go: `1.19.5`

**Additional context**
**Note:** The `mySetStruct` does not cause an error, only the original interface returning `map[string]struct{}`.
