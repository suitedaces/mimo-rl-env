## SegmentedControl.IconButton has no tooltip on hover (a11y issue)

We use `SegmentedControl.IconButton` to render an icon-only segmented control (e.g. a view-mode switcher with just icons, no labels). The `aria-label` is set on each button so screen readers announce them correctly, but sighted users get nothing on hover — there's no visible tooltip explaining what each icon means.

```tsx
<SegmentedControl aria-label="View mode">
  <SegmentedControl.IconButton aria-label="Preview" icon={EyeIcon} />
  <SegmentedControl.IconButton aria-label="Raw"     icon={FileIcon} />
  <SegmentedControl.IconButton aria-label="Blame"   icon={GitBranchIcon} />
</SegmentedControl>
```

Hovering any of these buttons shows no tooltip. For an icon-only control, this is a real accessibility/usability problem — without text labels, hover discoverability is the main way most users figure out what each segment does, and right now there's no fallback for them. The `aria-label` we already pass is the obvious thing to surface here.

It looks like there's even a `// TODO` comment in `SegmentedControlIconButton.tsx` from when tooltips were intentionally removed pending a Tooltip component remediation, so I assume bringing them back has been on the roadmap. Could we get this turned on?

A couple of related things that would be useful while you're at it:

1. Sometimes the `aria-label` is a short noun ("Preview") but we'd like to show a longer, supplementary explanation in the tooltip (e.g. "Render the file as HTML"). It would be nice to be able to provide that extra text without having to overload `aria-label` itself, since `aria-label` is what screen readers announce.
2. Depending on where the control sits in the layout, the default tooltip placement can collide with surrounding UI. Being able to nudge the tooltip direction per button would help.

Since this changes default rendering for an existing component and could affect downstream consumers, it would also be good to gate this behind something opt-in for a release or two before flipping it on by default.

For naming, I'd suggest the supplementary-text prop be called something like `description`, and the opt-in be a feature flag along the lines of `primer_react_segmented_control_tooltip`.
