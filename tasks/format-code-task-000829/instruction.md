I want `doorstop` with no subcommand to act as the project validation command. When I run it from a Doorstop working copy, it should load the tree, print a progress line like `validating items...`, and report traceability, review, outline, link, and external-reference problems with info, warning, or error severity.

I also want the top-level validation flags `--no-reformat`, `--reorder`, `--no-level-check`, `--no-ref-check`, `--no-child-check`, `--strict-child-check`, `--no-suspect-check`, `--no-review-check`, `--skip`, `--warn-all`, and `--error-all` to control which checks run and how issues are treated.

On success, if the tree has more than one document, it should print the drawn tree before exiting 0. If validation finds error-level problems, or the tree cannot be loaded, it should exit nonzero.
