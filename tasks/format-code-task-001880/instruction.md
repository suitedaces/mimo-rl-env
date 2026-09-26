## Problem Statement

I'm using a Bootstrap theme with my Vizro dashboard and the page items in the left-side accordion are showing up as big solid blue primary buttons instead of looking like links in the sidebar. They also don't behave like links — I can't middle-click to open a page in a new tab, and the highlighting on the current page feels off when I navigate around. Can you take a look at how the accordion navigation is being rendered?

## Expected Outcomes

- Accordion navigation entries should behave like links in the sidebar: each page item should use link-style navigation semantics and expose the page URL as its target.
- Accordion page items should no longer receive Bootstrap primary button styling from the active theme.
- The highlighted accordion page item should follow the current browser location when navigating between pages.
- Moving between accordion pages should not leave the previously selected page visually highlighted.

## Implementation Notes

- The specific component composition, CSS organization, and validation location are up to the implementation, as long as the rendered accordion has link semantics, correct page targets, and location-driven highlighting behavior.
- Preserve the existing page registration and accordion grouping behavior while changing how individual page navigation entries are represented.
