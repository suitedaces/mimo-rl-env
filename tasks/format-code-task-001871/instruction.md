## Problem Statement

I'm rendering a table in the terminal and the alignment is off whenever there's CJK content mixed in. Narrowed it down to go-runewidth: `runewidth.StringWidth("\u3000")` comes back as 1, and the fullwidth ASCII stuff like `！？Ａ` in the U+FF01 range also reports as 1 per rune. These all render as two cells wide in every terminal/font I've tried, so my column math ends up short by exactly the count of those characters. Am I using the wrong API here, or is something off with how it's classifying these?

## Expected outcomes

- Fullwidth characters such as the ideographic space and fullwidth ASCII/punctuation examples above should be measured as two terminal cells by the public width APIs.
- The fix should apply to the relevant fullwidth character data used by the library, not only to the exact sample string in the report.
- The corrected behavior should remain consistent when the repository’s normal Unicode data update workflow is used.

## Implementation notes

The specific data representation, table layout, and validation location are up to the implementation. The fix should preserve existing public API behavior for unrelated characters while correcting the width classification for affected fullwidth characters.
