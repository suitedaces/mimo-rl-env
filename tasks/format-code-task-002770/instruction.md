# Add a Find-and-Replace engine

Our editor needs a working find-and-replace capability that operates on the document
behind an editor session. Please add a `FindAndReplaceManager` and make it reachable
from the library's public exports (i.e. it can be imported by name from the package
entry point, alongside the other editor utilities).

The manager is constructed with an editor session:

```js
let manager = new FindAndReplaceManager(editorSession)
```

It drives a search over the editable text of the document and lets the user step
through matches and replace them. The observable behavior must be:

## Searching

- `setSearchPattern(pattern)` sets the search term and (re)runs the search immediately.
- The search finds every **non-overlapping** occurrence of the pattern in the editable
  text of the document, scanning left-to-right. So searching `aa` in `aaaa` yields two
  matches.
- The pattern is matched **literally** — characters that are special in regular
  expressions (e.g. `.`, `*`, `(`) match themselves and nothing else.
- Searching is **case-insensitive by default**.
- An empty pattern (`''`) produces no matches.
- `getMatchCount()` returns the total number of matches currently found.

## Options

- `setCaseSensitive(flag)` controls case sensitivity. When enabled, only occurrences
  with identical casing match. Toggling it re-runs the search against the current
  pattern.
- `setWholeWord(flag)` restricts matches to whole words only — an occurrence matches
  only when it is bounded by a word boundary on both sides (so `foo` matches the
  standalone word `foo` but not the `foo` inside `foobar` or `food`). Toggling it
  re-runs the search.
- Both options default to off.

## Navigation

- Matches are ordered by their position in the document: by the order text blocks appear
  in the document body, and by character offset within each block.
- After a search that yields at least one match, the **first** match (in document order)
  is the current match.
- `getCurrentMatch()` returns the current match as an object with a `path` (the text
  property path, e.g. `['p1', 'content']`), a `start` offset and an `end` offset
  (character offsets into that property's text, with `end` exclusive). It returns `null`
  when there is no current match (no pattern, or no matches).
- `selectNext()` moves the current match to the next one in document order, wrapping
  back to the first after the last. `selectPrevious()` moves to the previous one,
  wrapping to the last from the first. With no matches these are no-ops.

## Replacing

- `setReplacePattern(replacement)` sets the replacement string. It does not change the
  current matches.
- `replaceNext()` replaces the current match in the document with the replacement
  string, then refreshes the matches against the modified document. The match that
  followed the replaced one (in document order) becomes the new current match, wrapping
  to the first if the replaced match was the last one, or `null` if no matches remain.
  With no current match it does nothing.
- `replaceAll()` replaces every current match in the document with the replacement
  string.

Replacements go through the editor session so they participate in the normal document
edit/undo flow.
