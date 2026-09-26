## Generate a single root component that composes nested layouts

Sapper supports nested layouts: a route like `/blog/[slug]` is rendered by walking a
chain of `_layout.svelte` components down to the leaf page component, with route data
("preloaded" props) attached at every level. Today each layout is responsible for
rendering the next component in the chain itself, which makes the data flow awkward.

I want the build step that emits the per-app **internal manifests** (the generated
client/server manifest modules that live in the project's internal output directory) to
*also* emit a single generated **root Svelte component** into that same internal
directory. This component takes a fully-resolved route (the components for each level and
their props) and renders the whole nested layout/page tree in one place, so individual
layouts no longer have to render their own children.

### What the generated component must do

The component is generated once per build and must be deep enough to render the
*deepest* route in the app — i.e. it must support up to N nested levels, where N is the
maximum number of layout/page parts across all of the app's pages.

It accepts these props:

- `segments` — an array of the current path's segments.
- `level0` — an object `{ props }` carrying the props for the app's **root layout**.
- `level1`, `level2`, … `levelN` — one prop per nesting level, each either `null` or an
  object `{ component, props, segment }`. `component` is the Svelte component constructor
  to render at that level, `props` are its props, and `segment` is its path segment.
  Every `levelI` (I ≥ 1) defaults to `null`.
- `error` and `status` — error information for the route.

Rendering rules:

- The app's **root layout component** is always the outermost element. It receives
  `segment={segments[0]}` plus the props from `level0` (spread onto it).
- The remaining content is rendered *inside the root layout* (i.e. in its default slot):
  - If `error` is truthy, render the app's **error component**, passing it `error` and
    `status`, and do **not** render any of the page-level components.
  - Otherwise render the page chain as nested components: `level1`'s component contains
    `level2`'s component, which contains `level3`'s, and so on, down to the deepest level
    that is provided. Every non-leaf level in this chain receives `segment={segments[i]}`
    (where `i` is that level's number) plus its own `props` spread onto it; the deepest
    rendered level just gets its `props`. A level is only rendered when its prop is
    non-`null`, so a route that is shallower than the app's maximum depth (a trailing
    `levelI` of `null`) renders only the levels that are actually supplied.

The root layout and error components are the ones the app already resolves as its layout
and error pages; the generated component must import and use them.

Wire this generation into the existing manifest-generation step so the component file is
written alongside the other generated internal files whenever the manifests are
(re)generated. The generated component must be valid Svelte.
