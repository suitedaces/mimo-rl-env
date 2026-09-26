# Collect the custom code a page actually uses

Our SSR package (`@toddledev/ssr`) renders pages from a `ProjectFiles` object. A page can use
custom JavaScript **formulas** and **actions** that are defined either directly in the project
(`files.formulas`, `files.actions`) or inside installed packages
(`files.packages[name].formulas`, `files.packages[name].actions`). In every case the formulas /
actions are stored in a record keyed by their name.

Right now the server has no way to tell which of these a given page actually needs, so it cannot
ship a trimmed bundle of custom code per page. I want a reusable helper for that.

Add a module `custom-code/codeRefs.ts` to the SSR package source that exports two functions:

- `takeReferencedFormulasAndActions({ component, files })`
- `hasCustomCode(component, files)`

## `takeReferencedFormulasAndActions`

It takes an object with an optional entry `component` (a `Component`, or `undefined`) and the
`files` (`ProjectFiles`), and returns the referenced custom code **grouped by origin**:

- Project-level formulas/actions live under the key `__PROJECT__`.
- Each package's formulas/actions live under that package's name (its key in `files.packages`).
- Every group has the shape `{ actions, formulas }`, where each is a record mapping the original
  key to the original formula/action definition.
- The `__PROJECT__` group is **always present**, even when it is empty.

Behavior:

- When `component` is `undefined`, return *everything*: all of `files.formulas` / `files.actions`
  under `__PROJECT__`, and, for every package, that package's complete set of formulas and actions
  under its name.

- When a `component` is given, return *only what is reachable from it*, following references
  transitively through every component it includes — both project components and package
  components:
  - Under `__PROJECT__`, include exactly the project formulas and actions that are referenced.
  - Include a package only when at least one of its formulas or actions is referenced; within an
    included package, include only the referenced ones. Packages with nothing referenced are
    omitted entirely.
  - A reference to a formula or action that does not exist in `files` contributes nothing.

A formula/action counts as "referenced" when the entry component, or any component reachable from
it, uses it. Package formulas/actions are matched within the package they belong to.

## `hasCustomCode`

`hasCustomCode(component, files)` returns `true` when the given component references at least one
formula or action (project or package), and `false` otherwise.
