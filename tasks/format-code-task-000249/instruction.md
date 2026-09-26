# Add a ComponentBuilder for the Next.js package

Our Next.js integration currently wires up a single static "component factory" that maps
component names to React components. That approach is too rigid: an app may register components
that are loaded statically, components that are imported dynamically (lazy), and modules that
also expose component-level data-fetching hooks. We need a small building block that can produce
the right factory for each of these cases from one registry.

Add a `ComponentBuilder` class to the `sitecore-jss-nextjs` package source. It must be a named
export importable as `ComponentBuilder`. It is constructed with a config object whose `components`
property is a `Map` keyed by component name. Each map value is one of:

- a **static module** — a plain object holding one or more named exports, e.g. a Next.js style
  `default` export, an SXA style `Default` export, the optional data-fetching hooks
  `getStaticProps` / `getServerSideProps`, and/or any number of additional named component exports;
- a **lazy module** — an object exposing a `module()` function that returns the module (typically a
  promise that resolves to it);
- a **lazy component** — an object exposing an `element(isEditing?)` function that returns the React
  component to render.

The class exposes two methods, each of which returns a *factory function* built from the registry:

### `getModuleFactory()`

Returns a function `(componentName) => module`. Given a name it resolves the full module so callers
can reach its data-fetching hooks:

- unknown name → `null`;
- lazy module (has a `module` function) → the result of invoking that function;
- static module → the stored object itself.

### `getComponentFactory(config?)`

Accepts an optional config object with an optional `isEditing` boolean (treat a missing config as
`{}`). Returns a function `(componentName, exportName?) => Component` that resolves to the React
component for a name:

- unknown name → `null`;
- lazy component (has an `element` function) → the result of invoking `element(isEditing)`, passing
  the configured editing flag straight through;
- static module:
  - when an `exportName` other than the SXA default name `"Default"` is supplied, return that named
    export from the module;
  - otherwise return the module's default component, preferring the SXA `Default` export, then the
    Next.js `default` export, and `null` if neither exists. (Asking for the `"Default"` export name
    explicitly follows this same default-resolution rule.)

Each call to `getModuleFactory()` / `getComponentFactory()` must return a usable factory, and the
two factories must reflect the same registry the builder was constructed with.
