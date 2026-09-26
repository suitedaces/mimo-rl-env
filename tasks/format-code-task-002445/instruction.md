# Problem Statement

I’m hitting a couple of GUI edge cases that feel like bugs: if I pass an RGBA tuple into `UIWidget.with_background`, it later blows up like the background isn’t really a color object, and `UIBoxLayout` can crash when the available size on an axis ends up being zero. It would be nice if tuple colors worked the same way as normal colors, and if the layout just degraded gracefully instead of dividing by zero when there’s no space. Also, the color picker example seems to lay out the same color buttons strangely, like they’re being attached in more than one place.

# Expected outcomes

- Background colors:
  - `UIWidget.with_background(color=...)` should accept RGBA tuple-style color input and use it in the same way as other supported color objects.
  - Passing `None` as the background color should continue to represent no background rather than being converted into a color.

- Box layout edge cases:
  - `UIBoxLayout` layout calculations should not crash when the available size along a layout axis is zero or negative.
  - When there is no usable space along an axis, child sizing should degrade to each child’s minimum size instead of raising a division-related exception.
  - This zero-or-negative-size fallback should emit the warning message: `Container size is 0, cannot calculate sizes for children.`

- Color picker example:
  - The color picker example should avoid duplicate ownership/attachment of its palette buttons.
  - Each palette color button should appear once in the intended palette area without layout anomalies caused by being attached to multiple containers.

# Implementation notes

The exact validation location, helper structure, and layout calculation organization are up to the implementation. Preserve the existing public GUI APIs while making these edge cases behave consistently and safely.
