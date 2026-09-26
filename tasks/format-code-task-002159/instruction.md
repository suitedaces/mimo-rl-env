## rhc list commands crash when the result is empty

When I run an `rhc` command that's supposed to show me a list of things and I currently have nothing to list, the command crashes instead of printing an empty list / "no items" message.

Easy way to hit it: fresh account / fresh install, nothing created yet, just run:

```
$ rhc apps
```

It blows up rather than telling me I have zero apps.

As soon as I create one application, the same command works fine and prints the table as expected. So the problem is specifically the zero-results case — any list-style command that ends up with an empty result set seems to die instead of rendering a (presumably empty) table.

Would expect the tabular output to handle "no rows" gracefully — either print nothing, print just the header, or print some "no items" indicator — but not crash the command.
