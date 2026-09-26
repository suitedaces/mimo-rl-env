# Add a template-rendering core for the `create-module-federation` scaffolder

We're building a `create-module-federation` scaffolding CLI that generates a new project by
copying a template directory into a target directory. Before wiring up the interactive prompts,
we need the engine that actually materializes a template on disk.

Please add a new package at `packages/create-module-federation`. Its entry point
(`src/index.ts`) must export an async function `renderProject` that copies a template directory
tree into a destination directory, rendering template files along the way.

## API

```ts
renderProject(options: {
  templateDir: string;                 // directory to read the template from
  targetDir: string;                   // directory to materialize the project into
  data?: Record<string, unknown>;      // values used when rendering template files
  override?: boolean;                  // default false
}): Promise<{ written: string[]; skipped: string[] }>
```

## Behavior

- **Recursive copy.** Every *file* found anywhere under `templateDir` (at any nesting depth)
  produces a corresponding file under `targetDir` at the same relative path. Intermediate
  directories are created as needed. `targetDir` itself is created if it does not exist. Dotfiles
  and files inside hidden directories (e.g. `.gitignore`, `.npmrc`, `.vscode/settings.json`) are
  included, and empty files (e.g. `.gitkeep`) are reproduced as empty files.

- **Template files.** A file whose name ends with `.handlebars` is a *template*: its contents are
  rendered (see below) and it is written to the target with the trailing `.handlebars` removed
  from the filename — only the final `.handlebars` segment is stripped (so
  `package.json.handlebars` → `package.json`, `module-federation.config.ts.handlebars` →
  `module-federation.config.ts`, `foo.handlebars` → `foo`).

- **Other files** are copied verbatim, byte-for-byte. Their contents are never interpreted as a
  template even if they happen to contain placeholder-looking text.

- **Placeholder rendering.** Inside a template file, a placeholder is written as `{{ expr }}`,
  where `expr` is a dot-separated path of identifiers and any surrounding whitespace inside the
  braces is ignored (`{{name}}`, `{{ name }}` and `{{  name  }}` are equivalent). Each occurrence
  is replaced by the value obtained by resolving the dot path against `data`, converted to its
  string form (numbers and booleans are stringified). Repeated and multiple placeholders on a
  single line are all substituted.

- **Missing values.** If a placeholder in a template references a path that cannot be resolved
  against `data` (including the case where `data` is omitted), `renderProject` rejects with an
  `Error` whose message includes the unresolved expression (the dot path as written).

- **Overwrite policy.** Before writing each output file, if a file already exists at that target
  path:
  - with `override` falsy (the default), the existing file is left untouched and its
    target-relative path is reported in `skipped`;
  - with `override` truthy, the existing file is overwritten and its target-relative path is
    reported in `written`.

  Output files that do not yet exist are always written and reported in `written`.

- **Return value.** Resolves to `{ written, skipped }`, where each is the list of
  target-relative file paths (relative to `targetDir`, using `/` separators) that were written
  or skipped respectively. The order of the lists is not significant. Rendered template files
  appear under their stripped names.

An empty template directory yields `{ written: [], skipped: [] }`.
