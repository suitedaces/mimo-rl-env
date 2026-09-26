# Add an `ohm` command-line tool with a `generateRecipes` command

This is a monorepo. We have a `packages/cli` workspace set up for an `@ohm-js/cli`
package, but it has no source yet. I'd like you to build the first version of the
command-line tool for Ohm.

The tool is driven by a single programmatic entry point that the package exports as a
function named `ohmCli`:

```js
const {ohmCli} = require('@ohm-js/cli'); // i.e. the package's main entry point
ohmCli(args, options);
```

`args` is the list of command-line arguments **as a user would type them** (no
`node`/script prefix), e.g. `['generateRecipes', 'src/*.ohm']`. `options` is an optional
object used to control/observe behavior programmatically:

- `cwd` — base directory that glob patterns are resolved against and that output files
  are written under. Defaults to the process's current working directory.
- `noProcessExit` — when truthy, invalid usage raises an `Error` instead of terminating
  the process (so it can be tested). The thrown error's message must identify the
  problem: it names the missing argument, the unrecognized option, or the unknown
  command, respectively.

`ohmCli` runs the requested command and returns whatever that command produces.

## The `generateRecipes` command

`generateRecipes <patterns...>` takes one or more glob patterns and turns every matching
Ohm grammar file into a standalone "recipe" module. It requires at least one pattern; if
none is given it is a usage error.

For each matched file:

- Only files whose extension is `.ohm` are processed. Any other file that happens to
  match a pattern is ignored.
- The grammar in the file is compiled, and a recipe module is produced for it. The output
  path is the source path (relative to the base directory) with `-recipe.js` appended —
  so `arithmetic.ohm` becomes `arithmetic.ohm-recipe.js`, and a nested `e/f/g.ohm` becomes
  `e/f/g.ohm-recipe.js`.
- A recipe is a **self-contained CommonJS module**: requiring it returns the compiled
  grammar, ready to use (e.g. `.match(...)`), without needing the original `.ohm` file.

The command returns an object with a `filesToWrite` property: a mapping from each output
path (relative to the base directory) to that file's text contents.

A global `-n`, `--dryRun` flag controls whether anything touches the disk:

- Normally, each output file is actually written under the base directory (creating it as
  needed), **and** the returned `filesToWrite` describes them.
- In dry-run mode, nothing is written to disk, but the returned `filesToWrite` still
  describes exactly what would have been written.

The return value of `generateRecipes` is what `ohmCli` returns when that command runs.
