I want a `tools/filter.py` command that prepares one thread's raw ftracer event stream for the next report-generation stages. The command should be invoked as `tools/filter.py -f trace.txt`, where each input row is pipe-delimited as `TYPE|FUNC|CALLER|CURRENT_SYMBOL_PATH|CALLER_SYMBOL_PATH` and `TYPE` is `E` for function entry or `X` for function exit.

For a balanced input like:

`X|stale|caller||`
`E|main|root|/bin/app|/bin/app`
`E|child|main|/bin/app|/bin/app`
`X|child|main|/bin/app|/bin/app`
`X|main|root|/bin/app|/bin/app`

it should drop the leading exit row and write this stdout with exit code 0:

`E|main|root|main|root|/bin/app|/bin/app`
`E|child|main|child|main|/bin/app|/bin/app`
`X|child|main|0x0|0x0||`
`X|main|root|0x0|0x0||`

Entry rows should preserve the function and caller addresses both as the event identifiers and as the lookup addresses, plus the two symbol-path fields. Exit rows should be emitted synthetically with `0x0|0x0||` lookup fields so later symbolization work can ignore exits.

If the nesting is broken, the command should still emit a balanced stream and warn on stderr. For input `E|outer|root||`, `E|inner|outer||`, `X|outer|root||`, stdout should include synthetic exits for `inner` and `outer`, stderr should include `Filter - Warning: Incorrect exit func: outer(3), expect: inner(2)`, and the process should exit 0.

If a processed row has an unknown type such as `Q|bad|row||`, the command should print `Filter - Warning: Incorrect type: Q at line 1, the type must be E or X` to stderr and exit non-zero. `tools/filter.py -h` should print `usage: filter.py -f trace.txt` to stdout and exit 0; running it with no arguments should print the same usage line and exit non-zero.
