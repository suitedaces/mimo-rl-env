# Add condition coverage to the JSON tracefile format

Modern GCC (14+) can emit *condition coverage* (a form of MC/DC) for each line,
on top of the existing line/branch/decision/call metrics. When gcov is invoked
with `--conditions --json-format`, every relevant line carries a list of
condition records that look like this:

```json
{
    "count": 8,
    "covered": 3,
    "not_covered_true": [0, 1, 2, 3],
    "not_covered_false": [0]
}
```

`count` is the total number of condition outcomes on that line, `covered` is how
many of them were exercised, and `not_covered_true` / `not_covered_false` list
the term indices whose true / false outcome was never taken.

gcovr already round-trips its own JSON tracefiles through `--add-tracefile`, but
it currently drops condition information. Teach gcovr to carry condition
coverage through its JSON pipeline and to report it.

## What needs to work

**Detailed JSON (`--json`).** A line in a gcovr JSON tracefile may carry an
optional `"gcovr/conditions"` key holding a list of condition records with the
four fields shown above. When gcovr reads such a tracefile and writes it back
out as JSON, the condition records must survive the round-trip unchanged:

- A line that has at least one condition emits `"gcovr/conditions"`; a line with
  no conditions must not emit the key at all.
- Each emitted record preserves `count`, `covered`, `not_covered_true` and
  `not_covered_false`. The index lists are emitted in ascending order, and the
  records keep the order of their condition index.

**Merging.** When the same line is read from several tracefiles (multiple
`--add-tracefile` options), its condition records are combined positionally.
Merging two records describing the same condition keeps the same `count`, while
a true/false outcome counts as covered if it was taken in *any* of the inputs.
In other words the merged `not_covered_true` is the intersection of the inputs'
`not_covered_true` lists (likewise for `not_covered_false`), and `covered` is
`count` minus the number of outcomes still uncovered.

**Summary JSON (`--json-summary`).** The summary must report aggregated
condition coverage the same way it reports branch coverage: each per-file entry
and the top-level footer gain `condition_total`, `condition_covered` and
`condition_percent`. Totals are summed over all reportable lines; the percent
follows the same rounding/clamping rules already used for the other metrics
(one decimal, capped at 99.9% unless everything is covered, and the
no-elements default — `null` per file, `0.0` in the footer). These three keys
are always present in the summary, exactly like the branch keys, even for
reports that contain no condition data at all.

Detailed reports for lines and files without condition data must otherwise be
unchanged.
