## Problem Statement

When I run `python ./sendto_silhouette.py --version` or `-V` from my packaging script, it tries to process an SVG and fails unless I pipe in a dummy SVG first. I’m just trying to read the extension version there, so the dummy input feels like a weird workaround. I also ran into an SVG with `viewBox="0,0,100,100"` that opens fine in Inkscape but makes this extension fail during processing.

## Expected Outcomes

- Version queries: `python ./sendto_silhouette.py --version` prints the extension version and exits successfully even when no SVG file argument is provided and nothing is piped on stdin.
- Short version queries: `python ./sendto_silhouette.py -V` provides the same standalone version-query behavior as `--version`.
- Packaging version discovery: repository packaging or distribution scripts that need the extension version can obtain it by invoking `python ./sendto_silhouette.py --version` directly, without piping placeholder SVG content into the command.
- SVG compatibility: SVG documents whose `viewBox` numeric fields are comma-separated, including commas without following spaces, are accepted for normal processing rather than failing at viewBox handling.

## Implementation Notes

The implementation may choose where to handle version-query short-circuiting and how to normalize SVG attribute values, as long as the command-line and SVG-processing behavior above is observable. Avoid making packaging scripts depend on synthetic SVG input solely to read the version.
