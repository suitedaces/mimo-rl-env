## Problem Statement

I'm seeing Jekyll generate a broken excerpt when a post has more than one Liquid block and the excerpt separator lands inside a later block—the build either hits a Liquid parse error or the page shows raw Liquid tags, even though the earlier block in the post is closed.

## Expected outcomes

- Generated excerpts should remain valid Liquid and render successfully when the excerpt boundary cuts through a Liquid block, including when other Liquid block content appears earlier in the same excerpt.
- Liquid block content that is already balanced within the excerpt should continue to render normally and should not be altered in a way that introduces duplicate or stray block endings.
- The same excerpt behavior should apply to registered custom Liquid block tags, not only to Jekyll’s built-in tags.
- When Jekyll changes an excerpt to make it renderable, the warning should make clear which document/excerpt was affected, refer to the excerpt separator involved, describe that the generated excerpt was adjusted, and continue giving users guidance about defining their own excerpt or excerpt separator in front matter.

## Implementation notes

- The specific parsing approach, data structures, and location of the excerpt-adjustment logic are up to the implementer.
- Preserve existing excerpt behavior outside the described Liquid-block truncation cases, including normal rendering and handling of content after the excerpt separator.
