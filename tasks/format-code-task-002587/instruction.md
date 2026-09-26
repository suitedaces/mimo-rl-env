## Cell text overflows its column when the column is very narrow

I've been hitting some display glitches with narrow columns. The drawn cell text ends up wider than the column itself and spills onto the next column, so the whole row's alignment looks broken until I widen the column again.

Some specific shapes that reliably trigger it for me:

- A column with CJK / fullwidth characters squeezed down to width 1 or 2. The first character drawn is a fullwidth one and it already takes 2 cells, so it pokes past the column boundary.
- A column that holds dict / list values (i.e. an `anytype` column where the row value is something like `{'a': 1, 'b': 2}` or `[1, 2, 3]`). Same thing — when I shrink the column it doesn't seem to be clipped down to the requested width.
- Setting `disp_truncator` to a multi-character string like `"..."` instead of the default single ellipsis. Once the truncator is more than one cell wide, the truncated cell ends up wider than the column — looks like only one trailing character gets dropped to make room for the truncator, which isn't enough when the truncator (or the trailing char) is itself wide.

Repro is roughly: open any sheet with one of the above (paste in some Chinese/Japanese text, or load a JSON file with nested dicts), then `_` / manual resize the column down to 1–3 cells wide. The displayed text is visibly wider than the column.

Expected: whatever the column width N is, the drawn cell never occupies more than N terminal cells. If there isn't enough room to even fit the truncator, I'd rather just see the column truncated to nothing than have it bleed into the neighbour.

I also ran into a related crash when I tried to format one of those dict/list values without a width set (calling `formatValue(val)` with no `width` argument from a plugin) — it blows up inside the clipping code instead of just giving me the unclipped string back.
