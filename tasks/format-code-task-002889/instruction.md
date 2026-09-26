# Problem Statement

Right now FawltyDeps only lets me point at an external TOML file for my custom dep-to-import mappings via `--custom-mapping`, but I'd really love to just declare a couple of these mappings inline in my `pyproject.toml` so I don't have to keep a separate file around for one or two packages. Could there be something like a `[tool.fawltydeps.custom_mapping]` section where I can write `my-package = ["mpkg"]`? And if I do still have a mapping file, it'd be nice if both just got combined rather than one overriding the other.

# Expected outcomes

- CLI custom mapping file option:
  - Users can pass an external custom mapping TOML file with `--custom-mapping-file FILE_PATH`.
  - The previous `--custom-mapping` command-line option is no longer accepted.

- Inline pyproject configuration:
  - Users can declare dependency-to-import mappings in a `[tool.fawltydeps.custom_mapping]` section of `pyproject.toml`.
  - A configured inline mapping such as `my-package = ["mpkg"]` is used when resolving whether declared dependencies correspond to observed imports.

- Combining mapping sources:
  - If both an external mapping file and `[tool.fawltydeps.custom_mapping]` are provided, mappings from both sources are considered.
  - If both sources define the same package according to FawltyDeps’ normal package-name matching rules, the import names from both sources are combined so that all listed import names can resolve that package.

- File validation:
  - Inline-only configuration should work without requiring an external mapping file.
  - If an external mapping file path is provided but is invalid, the existing invalid-file behavior is preserved.

# Implementation notes

- The exact internal representation, parsing flow, and merge mechanism are up to the implementer.
- Preserve existing dependency resolution behavior except where custom mapping inputs now add or combine user-provided mappings.
- Keep validation behavior focused on user-provided mapping files; inline-only configuration should not require an external file.
