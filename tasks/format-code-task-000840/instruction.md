Questions: check if type is assignable to other
Need a bit of help here: how do I check if types assignable to one other?

Scenario 1: I have two nodes, I can get their types via `getType()`. How do I check if A is assignable to B and if B is assignable to A?

Scenario 2: I have one node, and I want to check if it's assignable to custom type that I will conclude based on a string (template in a framework). To give context, user does something like (let's assume Angular syntax for familiarity) `*ngIf="foo"`. In my framework, `ngIf` doesn't exist runtime and there's no `boolean` type anywhere where I can `getType` it -- so how can I create it? What about more complex cases?

I was expecting some `Type` constructors, but browsing through `.d.ts` files gives me nothing. Also _assignable_ gives no results. I see the docs mention the type checker but I don't see anything useful there either based on method names.

Any pointers would be appreciated. :smile:
