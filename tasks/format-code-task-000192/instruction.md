我现在在 RunPausedSplash 里为了做 Figma 上那两个 LargeButton 样式，只能在页面里写一堆覆盖样式，还要单独处理 icon 颜色，感觉很脆。能不能让 LargeButton 自己就支持透明白边白字的按钮，以及白底红字的警示按钮，这样“Cancel run”和“Launch recovery mode”就不用各自 hack 样式了。

Expected outcomes:
- `LargeButton` exposes reusable `buttonType` variants named `onColor` and `alertAlt`.
- `buttonType="onColor"` renders as a transparent, on-colored button with white label/icon treatment and a white outline; its disabled state keeps the on-color intent while using disabled styling.
- `buttonType="alertAlt"` renders as the alternate alert treatment with a white background and red label/icon treatment; its disabled state uses disabled styling.
- `LargeButton` callers should no longer use `iconColorOverride`; icon color should come from the selected button variant and disabled state.
- In `RunPausedSplash`, “Cancel run” uses the standard alternate alert LargeButton treatment, and “Launch recovery mode” uses the standard on-color LargeButton treatment, instead of page-local color/icon/border overrides.

Implementation notes:
- The concrete CSS organization, token lookup, helper structure, and component internals are up to the implementation.
- Keep existing `LargeButton` variants working as before, except where shared disabled styling must remain consistent with the variant-driven icon/text behavior.
