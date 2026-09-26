# Problem Statement

I'm using Tabs purely as a link-based navigation bar, and on routes where none of the tabs match the current URL, I want to show no active tab at all — but right now `index` only takes a number, so I can't express "nothing selected" without it complaining or just highlighting some random tab. It'd be great if I could pass something like `false` to mean no tab is active and have the indicator just not show up. Also, while I'm at it, if I ever pass an index that's out of range it currently blows up with an error instead of just doing nothing, which feels a bit harsh.

# Expected Outcomes

- **No selected tab state**: `Tabs` accepts `index={false}` as a valid value to explicitly represent that no `Tab` is selected.
- **No active indicator**: when `Tabs` receives `index={false}`, no tab is shown as active and the active-tab indicator is not visibly displayed.
- **Invalid index robustness**: when `Tabs` receives a numeric `index` that does not correspond to an available tab, rendering and updates should not throw.
- **Invalid index feedback**: invalid numeric indexes should produce development-time feedback that identifies the invalid index.
- **Unresolved selection safety**: rendering and updates should remain safe when the currently requested selected tab cannot be resolved, and should avoid showing an active indicator in that state.

# Implementation Notes

- Keep the existing public `Tabs` API behavior intact aside from allowing the explicit no-selection state.
- The exact internal control flow, data structures, measurement helpers, and fallback location are implementation details.
- Prefer observable component behavior over coupling the solution to a particular internal helper shape.
