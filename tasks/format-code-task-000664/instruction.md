## SuppressWarningsHolder: align Javadoc with xdoc

Part of #5750.

While going through the checks to align Javadoc with the corresponding xdoc page, I noticed `SuppressWarningsHolder` is out of sync. Its Javadoc currently is just a one-liner:

> Maintains a set of check suppressions from {@link SuppressWarnings} annotations.

…whereas the xdoc page (`config_annotation.xml`, `SuppressWarningsHolder` section) has a full description, the `aliasList` property documented in the properties table, and several usage examples covering the `checkstyle:` prefix, the alias mechanism, and the `"all"` argument.

A user reading the class Javadoc in their IDE gets almost nothing, while a user reading the website gets the real documentation. The two should match, the same way we've been doing it for other checks in #5750.

While we're at it, the xdoc entry for this check could also use a pass to bring it in line with how the other check pages in `config_annotation.xml` are written (the `aliasList` row, the surrounding examples section, etc., feel a bit inconsistent with the rest of the page).

No code behavior changes — this is a documentation alignment only.
