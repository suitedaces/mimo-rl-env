Do you have any example how to setup gin with v9 and modifiers/scrubbers?

Coming from other languages this seems like a nice way to handle it without writing a custom validator/processor for every user input. The only thing is, at least for me as a newish guy to golang, I have no clue how to integrate it with gin. The validator-upgrade.go is somewhat understandable, but I'm totally lost on how and where to hook into. Where does gin and the validator do the stuff and how do I inject mold.Transformer and actually execute it, prior to the validator (binding) run?

Can you give any hints or is there any help page I've missed?

`Struct(ctx context.Context, v interface{}) error` func doesn't work on slice fields.

Here is the example code (inspired by `_examples/full/main.go`):
```
import (
	"context"
	"fmt"
	"log"
	"reflect"

	"github.com/go-playground/mold/v3"
	"github.com/go-playground/mold/v3/modifiers"
)

type Address struct {
	Name  string `mod:"trim"`
	Phone string `mod:"trim"`
}

type User struct {
	Name    string           `mod:"trim"`
	Age     uint8
	Gender  string          `mod:"trim"`
	Email   string             `mod:"trim"`
	Address []Address
}

func main() {
        user := User{
		Name:   "test   ",
		Age:    50,
		Gender: "female",
		Email:  "test@test.com",
		Address: []Address{
			{
				Name:  "test   address    ",
				Phone: " 123 456  ",
			},
			{
				Name:  "test   address    ",
				Phone: " 123 456  ",
			},
		},
	}

        conform  := modifiers.New()
	if err := conform.Struct(context.Background(), &user); err != nil {
		log.Panic(err)
	}
	fmt.Printf("Conformed:%+v\n\n", user)
}
```

Output:
```
Conformed:{Name:test Age:50 Gender:female Email:test@test.om Address:[{Name:test   address     Phone: 123 456  } {Name:test   address     Phone: 123 456  }]}
```

So, `Name` and `Phone` fields of the Address struct weren't trimmed.

If I add `dive` tag to the `Address` field the `Struct` func will panic:
```
type User struct {
        ...
	Address []Address `mod:"dive"`
}
```

Panic:
```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x32 pc=0x10c0c19]

goroutine 1 [running]:
github.com/go-playground/mold/v3.(*Transformer).setByField(0xc000021ac0, 0x11cf500, 0xc0000160a0, 0x1176760, 0xc000021b00, 0x199, 0xc00018ae70, 0x0, 0x0, 0x0)
/Users/myuser/go/pkg/mod/github.com/go-playground/mold/v3@v3.0.0/mold.go:202 +0x79
github.com/go-playground/mold/v3.(*Transformer).setByField(0xc000021ac0, 0x11cf500, 0xc0000160a0, 0x115af80, 0xc00009adf8, 0x197, 0xc00018ae40, 0x0, 0x0, 0x0)
...
```

The reason for the panic is that the `dive` tag could not be used alone, so you'll have to add some tag after it (`endkeys` tag doesn't work as well).

The workaround for that issue is to register a dummy transform function:
```
func items(_ context.Context, _ *mold.Transformer, _ reflect.Value, _ string) error {
	return nil
}

...

conform.Register("items", items)
```

... and add a `mod:"dive,items"` tag to the slice field:
```
type User struct {
        ...
	Address []Address `mod:"dive,items"`
}
```

I think that the issue should be addressed either by fixing this in the lib or by adding that to the documentation.

What do you think?

P.S.
I can help with a PR if you need it.

Thanks.
