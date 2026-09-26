## Output of flattened file has inconsistent whitespace

When I run truffle-flattener over a few `.sol` files (either via the CLI with `--output` or by `require`-ing it as a library) and look at the resulting flat file, the whitespace looks off:

- There's a blank line at the very top of the output before the first `// File: ...` header.
- The amount of blank lines between consecutive files isn't always the same.
- The end of the file doesn't end cleanly with a single newline — sometimes there are extra blank lines, sometimes the last line has no trailing newline at all.

I noticed this when I tried to commit the flattened output to a repo: my editor kept "fixing" the file on save (POSIX expects every text file to end with exactly one newline), and a `diff` between two flattens of the same input wasn't as stable as I'd like.

Minimal repro:

```js
const flatten = require("truffle-flattener");

(async () => {
  const out = await flatten(["./contracts/A.sol", "./contracts/B.sol"]);
  console.log(JSON.stringify(out));   // inspect leading/trailing whitespace
})();
```

Same thing via the CLI:

```
$ truffle-flattener contracts/A.sol contracts/B.sol --output flat.sol
$ cat -A flat.sol   # extra blank lines visible at top / between files / at end
```

It would be nice if the flattener produced a clean, predictable output: no leading blank line, consistent separation between concatenated files, and a single trailing newline at the end. Same output whether it's written via `--output`, printed to stdout, or returned from the library entry point.

Also, there don't seem to be any tests covering the output format right now, so it'd be good to lock this down with some.
