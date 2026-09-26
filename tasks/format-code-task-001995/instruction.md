# Make the JUnit report reflect every Cucumber result status (and stop leaking state)

Our plugin turns Cucumber's JSON output into a JUnit XML report so CI servers can
consume the results. The JUnit generator takes the parsed Cucumber output (an array of
features, each with `elements` representing scenarios, each scenario with an ordered
list of `steps`) together with an options object that at least carries the `output`
file path to write, and writes a `<testsuites>` document: one `<testsuite>` per feature
and one `<testcase>` per scenario.

Right now the generator only understands two situations: a scenario containing a failed
step is recorded as a failure, and a scenario containing an undefined step is recorded
as skipped. Everything else — including scenarios that Cucumber reports as *pending* or
*ambiguous* — is silently emitted as a clean, passing test case, which misrepresents the
run on CI. On top of that, generating more than one report inside the same process
produces a corrupted document: each new report contains all the suites from the reports
generated before it.

Please make the report faithfully represent each scenario's outcome and make report
generation self-contained.

## Expected behavior

For each scenario, classify it from its steps and reflect that in its `<testcase>`:

- **Failure** — if any step failed, the test case is a failure (a `<failure>` child).
  The failure message must mention the failing step's name and the error message Cucumber
  reported for it. If several steps failed, every one of them must be mentioned.
- **Error** — otherwise, if any step is *ambiguous*, the test case is an error (an
  `<error>` child) whose message mentions the ambiguous step's name.
- **Skipped** — otherwise, if any step is *undefined* or *pending*, the test case is
  skipped (a `<skipped>` child).
- **Passed** — otherwise the test case has none of the above children.

These categories are strictly ordered: a failure outranks an error, which outranks a
skip, which outranks a pass. A scenario must never be tagged with more than one of these
outcomes, and the one chosen is the most severe present among its steps.

The structure and naming that already exist must be preserved: one suite per feature and
one case per scenario, with the suite name, the case `classname`, and the case name built
from the configurable `suiteNamePrefix`, `classNamePrefix`, and `scenarioNamePrefix`
options (defaulting to `"Feature: "`, `"Feature: "`, and `"Scenario: "` respectively). A
feature with no scenarios still yields its (empty) suite.

Finally, every invocation of the generator must produce a document describing only the
features passed to that call. Generating one report must not be polluted by, nor pollute,
any other report produced earlier or later in the same process.
