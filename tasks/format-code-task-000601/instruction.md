# Problem Statement

I'm using react-window with React.memo to wrap my row component, but my items are re-rendering on every scroll even when their data hasn't changed. Could you provide a built-in comparison helper I can drop into React.memo, and ideally something equivalent for class-based item components too, so my memoized rows actually skip these pointless re-renders?

# Expected outcomes

- Functional item renderers can import a top-level `areEqual` helper from `react-window` and use it as a `React.memo` comparison function.
- The functional helper skips updates when item renderer props are unchanged in shallow terms, including the rendered positioning/style values, even if wrapper objects are recreated between renders.
- The functional helper allows updates when any shallow style/positioning value or any other shallow prop value actually changes.
- Class-based item renderers can import a top-level `shouldComponentUpdate` helper from `react-window` and use it as an instance update check.
- The class helper skips updates when props are unchanged by the helper’s item-prop comparison and state is shallowly unchanged.
- The class helper allows updates when item props differ or when state shallowly differs.

# Implementation notes

- The helpers should be optional utilities and should not change the default rendering behavior of existing list or grid components.
- The exact internal organization, helper functions, file layout, and reuse between helpers are up to the implementation.
- Comparisons should remain shallow; deep equality is not required.
