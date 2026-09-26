# Problem Statement

I’m converting some SVGs with `svg2rlg`, and the colors defined in a `<style>` block don’t seem to show up at all — classes like `.red { fill: red; }` are ignored unless I move the fill onto each element. Could svglib handle basic stylesheet rules from `<style>` tags so SVGs that rely on class/id/element styling render correctly?

# Expected outcomes

- Stylesheet rules declared in SVG `<style>` elements are considered during `svg2rlg(...)` conversion rather than being ignored.
- Basic stylesheet selectors for SVG elements should affect rendered output when they match, including class selectors, id selectors, and element-name selectors.
- Stylesheet declarations for common presentation properties such as fill color, stroke color, and stroke width should be reflected in the generated ReportLab drawing when the matching SVG element does not already define that same property directly.
- Existing explicit presentation attributes on an SVG element take precedence over matching stylesheet declarations for the same property.
- The README Known limitations section should no longer state that stylesheets are unsupported; it should describe stylesheet support as experimental and direct users to report shortcomings.

# Implementation notes

- The exact parser, matching strategy, data structures, and point in the conversion pipeline where stylesheet declarations are applied are implementation choices.
- The implementation should preserve existing behavior for inline `style` attributes and direct SVG presentation attributes while adding support for basic rules from `<style>` blocks.
- Documentation wording may vary as long as it communicates the updated experimental-support status accurately.
