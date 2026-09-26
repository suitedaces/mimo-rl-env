I want the Go function `EstimateReadingTime(content string, defaultReadingSpeed int, cjkReadingSpeed int) int` in the `readingtime` package to estimate how many whole minutes an article takes to read. It should strip HTML/XML tags from `content` before counting, then return the ceiling of the detected text length divided by the appropriate reading speed.

For non-CJK text, it should count whitespace-separated words and use `defaultReadingSpeed`: `EstimateReadingTime("one two three four", 2, 500)` should return `2`, and `EstimateReadingTime("<p>one <strong>two</strong> three</p>", 2, 500)` should return `2`. For CJK-majority text, it should count Unicode runes and use `cjkReadingSpeed`: `EstimateReadingTime("漢字漢字漢字漢字", 200, 4)` should return `2`. Empty content should return `0`.

The function should be deterministic for the same inputs, should not mutate the input string, and should not perform filesystem, network, or global-state side effects.
