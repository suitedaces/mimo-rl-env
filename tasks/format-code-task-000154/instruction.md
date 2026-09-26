# Add a reports subsystem to the linter

Robocop can find issues, but right now there is no way to turn a run into different kinds of
output. I want to introduce a small **reports** subsystem so that a run can be summarized in
several ways (printing a version banner, dumping the found issues to a JSON file, etc.) and so the
set of active reports can be selected from configuration.

Please expose this through the package `robocop.linter.reports`.

## Selecting reports

Add a function `get_reports(configured_reports)` that takes a list of report names (strings) and
returns the enabled reports as an ordered mapping from report name to a report instance. Each
report instance must expose its own `name`. The selection rules:

- The returned mapping preserves the order in which names were requested and never contains
  duplicates (requesting the same report twice yields a single entry).
- The literal name `"all"` enables every report that is marked as a *default* report. Reports that
  are not default (for example `json_report` and `compare_runs`) are **never** pulled in by
  `"all"`; they can only be enabled by naming them explicitly. `"all"` may be combined with
  explicit names, e.g. `["all", "json_report"]`.
- Requesting a name that does not correspond to any known report raises
  `robocop.linter.exceptions.InvalidReportName`, and the raised error message must mention the
  offending name.
- The literal name `"None"` switches reports off: the result contains only the always-on internal
  `return_status` report, regardless of any external reports also requested in the same call. The
  one exception is that if `internal_json_report` was also explicitly requested, it is preserved
  alongside `return_status`.

## Reports that must exist

Reports are addressed by name through `get_reports`. The following named reports must be available:

- **`version`** — a default report whose `get_report()` returns a non-empty string that includes
  the installed Robocop version.
- **`json_report`** — a non-default report that collects issues handed to it via
  `add_message(message)` and, when `get_report()` is called, writes them as a JSON array to a file.
  Each issue is written in the same JSON form that an issue serializes to (i.e. the dict returned by
  the message's `to_json()`), and the array preserves the order in which issues were added. By
  default the file is named `robocop.json` and created in the current working directory, and
  `get_report()` returns a confirmation string that mentions the output path. The report is
  configurable through `configure(name, value)`:
  - `configure("report_filename", "<name>")` changes the output file name.
  - `configure("output_dir", "<dir>")` changes the directory the file is written to (the directory
    is created if it does not exist).
  - Any other parameter name passed to `configure` raises
    `robocop.linter.exceptions.ConfigGeneralError`.
- **`return_status`** — an internal report that is always kept under the `"None"` rule above and is
  also included by `"all"`.
- **`compare_runs`** and **`internal_json_report`** — non-default reports that exist but are not
  pulled in by `"all"`.

A report that does not recognize a configuration parameter should reject it by raising
`robocop.linter.exceptions.ConfigGeneralError`.
