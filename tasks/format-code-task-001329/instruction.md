### Feature request: integrate the `exptostd` linter

There's a small static-analysis tool, [`exptostd`](https://github.com/ldez/exptostd), that flags usages of functions from `golang.org/x/exp/maps` and `golang.org/x/exp/slices` that can now be replaced by their counterparts in the Go standard library (`maps`, `slices`, and the `clear` builtin) since Go 1.21 / 1.23.

For example, code like:

```go
package foo

import (
	"fmt"

	"golang.org/x/exp/maps"
)

func foo(m map[string]string) {
	clone := maps.Clone(m)
	fmt.Println(clone)
}
```

should be reported and replaced by the stdlib equivalent:

```go
package foo

import (
	"fmt"
	"maps"
)

func foo(m map[string]string) {
	clone := maps.Clone(m)
	fmt.Println(clone)
}
```

It would be very useful to have this available as a managed linter in golangci-lint so projects can keep their `x/exp` usage in check and migrate off of it as their minimum supported Go version moves up. Please plug it into the standard linter registration so it can be enabled/disabled like any other linter through `.golangci.yml`, with the JSON schema and reference config updated accordingly so editor tooling recognizes it.
