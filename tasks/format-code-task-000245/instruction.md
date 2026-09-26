## `IndexFilters` keyboard shortcut can't be turned off, and its tooltip always advertises it

I'm embedding the `IndexFilters` component in a page that has its own keyboard handling. I noticed that whenever the user presses `F` anywhere on the page (outside of an input), `IndexFilters` grabs focus and switches into search/filter mode. This conflicts with shortcuts I want to handle myself, and in some contexts I simply don't want a global single-letter shortcut hijacking keystrokes at all.

Looking at `IndexFiltersProps`, I don't see any prop to opt out of this behavior. The keydown handler inside `IndexFilters` always runs.

There's a related problem with the tooltip on the search/filter toggle button. The default tooltip text is something like:

> Search and filter (F)

The `(F)` is hard-coded into the localized strings (across all of the `locales/*.json` files) because it's part of the same single translation key used for the tooltip. So even in cases where pressing `F` shouldn't do anything, the tooltip still tells users it will — which is wrong / misleading.

I can override the tooltip via `filteringAccessibilityTooltip`, but that only patches the symptom on a single instance; the shortcut itself still fires, and every consumer that wants the same behavior has to know to override the string in every supported language.

### What I'd like

A way for the consumer of `IndexFilters` to disable the built-in keyboard shortcut behavior. When it's disabled:

- pressing `F` outside of inputs should no longer cause `IndexFilters` to enter search/filter mode,
- the default tooltip on the search/filter toggle button should stop advertising the `(F)` shortcut (and this should apply automatically across all supported locales, without each app having to ship its own override string).

The current behavior (shortcut on, tooltip mentions `(F)`) should remain the default so existing usages aren't affected.

I'd expect this to be exposed as a new boolean prop on `IndexFilters`, something like `disableKeyboardShortcuts`.
