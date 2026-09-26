## `~` (bitwise NOT) on integers fails to transpile

I was trying to transpile a small Python snippet with pytago that uses the bitwise NOT operator and it crashes instead of producing Go.

Minimal repro (`bitwisenot.py`):

```python
def main():
    yeah = 9
    yeah &= ~0x3
    print(yeah)

if __name__ == '__main__':
    main()
```

Running it through pytago bombs out — no Go output is produced. Other unary ops on the same kind of code (e.g. `-x`, `not x`) seem to work fine, it's specifically `~` that pytago refuses to handle.

I'd expect pytago to translate `~` on integers into the equivalent Go bitwise complement, so that the snippet above transpiles into something like:

```go
package main

import "fmt"

func main() {
	yeah := 9
	yeah &= ^3
	fmt.Println(yeah)
}
```

i.e. Python's `~expr` → Go's `^expr` as a unary operator. Right now I have to hand-edit any code that uses `~` before feeding it to pytago, which is awkward when the input has a lot of bit-twiddling. Could `~` be supported as part of the unary-operator translation?
