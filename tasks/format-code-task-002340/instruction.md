Change Function to FunctionReference
Right now the `Function` production defines the grammar of function names. It's a specialized version of the `Identifier` production. It's also used directly as a `callee` in `CallExpression`. This is a deviation from how we reference things in other parts of the syntax:

- `message.attr` is `AttributeExpression {ref: MessageReference {id: Identifier}, ...}`,
- `-term.attr` is `AttributeExpression {ref: TermReference {id: Identifier}, ...}`,
- but: `FUNC()` is `CallExpression {callee: Function, ...}`.

Let's unify this as:

    CallExpression {callee: FunctionReference {id: Identifier}, ...}
