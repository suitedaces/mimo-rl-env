### Shell completion still triggers when `--` is present in the argument list

My app has `EnableBashCompletion: true` and I rely on `--` as the conventional
POSIX separator between flags and positional arguments (everything after `--`
should be treated as a plain positional, not as something the parser/completer
should reason about — see e.g. https://unix.stackexchange.com/a/11382).

The problem: when the command line contains `--`, urfave/cli still goes down
the shell-completion path and emits completion suggestions for tokens that
appear after the `--`. From the user's point of view those tokens are
explicitly opaque positional arguments — there is nothing to complete there,
and offering flag/command suggestions for them is wrong.

Concrete example of the kind of invocation I'm talking about:

```
$ myapp -- somepositional<TAB>
```

Even though `--` was passed, completion machinery still kicks in.

Expected: as soon as `--` appears anywhere in the arguments, urfave/cli
should stop treating the invocation as a completion request and just leave
the remaining tokens alone as positional arguments, consistent with how
basically every other POSIX-style tool handles `--`.
