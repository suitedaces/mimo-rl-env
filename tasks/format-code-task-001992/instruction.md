# Problem Statement

I’m hitting a couple of odd cases while rendering some DXFs: `Bezier4P.approximate(0)` blows up with a `ZeroDivisionError`, and text entities whose content is only spaces or tabs still get measured/rendered by the matplotlib/pyqt drawing backends. I also noticed that when an `INSERT` expands to virtual entities that get skipped, nothing shows up in the frontend skipped-entity log, so it’s hard to tell what disappeared.

# Expected outcomes

- Bezier approximation:
  - `Bezier4P.approximate(segments)` should reject non-positive segment counts with a clear caller-facing exception instead of failing later with a division-by-zero error or returning an odd partial approximation.
  - Valid positive segment counts should continue to produce the same approximation vertices as before.

- Drawing backend whitespace handling:
  - The matplotlib and pyqt drawing backends should treat text made only of whitespace characters as having no drawable content.
  - Such whitespace-only text should not be rendered by backend text drawing.
  - The backend text-width measurement for whitespace-only input should report zero width.
  - Non-empty text that includes leading, internal, or trailing whitespace should continue to be handled as drawable/measurable text according to the existing rendering behavior.

- Skipped virtual entities from inserts:
  - When the drawing frontend expands an `INSERT` and a virtual entity is skipped during that expansion, the skipped entity should be reported through the frontend’s existing skipped-entity logging path.
  - Existing drawing of insert attributes and drawable virtual entities should continue to work.

# Implementation notes

- The exact validation location, control flow, and helper structure are up to the implementer.
- The fix should preserve the existing public rendering and geometry APIs while making the above edge cases observable through their normal external behavior.
- Do not rely on a particular backend internals layout; the intended behavior is defined by drawing, measuring, approximation, and frontend skip-log results.
