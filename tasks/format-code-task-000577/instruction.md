I've run into two issues while configuring wsl for our codebase.

## 1. `AllowCuddleDeclaration` doesn't seem to cover the common cases

I turned on `AllowCuddleDeclaration` because I want to be able to put a `var` declaration right next to the line that uses it. But I still get warnings on patterns like:

```go
var foo string
foo = "some value"
```

→ `assignments should only be cuddled with other assignments`

```go
var server = NewServer()
server.Start()
```

→ `expressions should not be cuddled with declarations or returns`

I'd expect that once I've opted in to cuddling declarations, follow-up lines that initialize or use the just-declared variable would be allowed too. Otherwise the option only helps for stacking multiple `var` lines together, which is a pretty narrow use case.

## 2. `ForceCuddleErrCheckAndAssign` is awkward with multi-line assignments

With `ForceCuddleErrCheckAndAssign` enabled I get pushed toward writing:

```go
result, err := someFunc(
    "argument one",
    "argument two",
    "argument three",
)
if err != nil {
    return err
}
```

This is fine for short assignments, but when the call producing the error spans many lines I really want a blank line between the closing paren of the call and the `if err != nil` — visually the assignment block and the error handling block are two distinct things, and gluing them together makes the code harder to read.

So in this case:

```go
result, err := someFunc(
    "argument one",
    "argument two",
    "argument three",
)

if err != nil {
    return err
}
```

wsl complains because the err check isn't cuddled with the assignment, but I don't think the rule should fire when the assignment itself is multi-line. For single-line assignments I'm happy to keep the strict cuddling requirement.

Could both of these be addressed?
