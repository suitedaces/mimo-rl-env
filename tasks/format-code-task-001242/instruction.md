`--print-summary` and `--decisions`
**Describe the bug**
`gcovr --decisions --print-summary` prints:

```
lines: 90.1% (13347 out of 14816)
functions: 91.2% (2338 out of 2565)
branches: 56.9% (14099 out of 24788)
calls: 0.0% (0 out of 0)
```

i.e., a summary of decision coverage is *not* printed.
On the other hand, the "calls:" line is always printed, regardless of the `--calls` option.

**Expected behavior**
* Show decision coverage summary when `--decisions` is specified.
* Do not print (nonsensical) calls coverage unless `--calls` is specified.

**Desktop (please complete the following information):**
 - OS: Linux
 - GCC version 12.2.0
 - GCOVR version 6.0
