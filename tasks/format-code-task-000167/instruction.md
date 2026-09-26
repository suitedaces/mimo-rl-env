## Problem Statement

我这边嵌套打开两个 NG-ZORRO Modal，第二个 Modal 配了 `nzZIndex`，内容层确实在上面，但它的遮罩看起来还压不住前一个 Modal，检查 DOM 发现 backdrop 的 `z-index` 还是默认值；如果同时用了 `nzMaskStyle`，更新遮罩样式后也是这个现象。

## Expected outcomes

- Modal instances configured with `nzZIndex` should apply that stacking level consistently to the visible modal and its associated mask/backdrop, so a later or higher-level modal mask can cover lower-level modals.
- When `nzMaskStyle` is present or updated on a modal that also has `nzZIndex`, the mask/backdrop should continue to reflect the configured `nzZIndex` rather than falling back to the default mask stacking level.
- Updating a modal’s `nzZIndex` after it has been opened should update the mask/backdrop stacking level together with the modal content stacking level.

## Implementation notes

- The exact place where the style is applied and the internal structure used to keep modal and mask styles in sync are implementation details.
- Preserve existing modal behavior other than the externally observable stacking behavior described above.
