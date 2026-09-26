## Coverage reports use internal Cadence location IDs instead of source file paths, breaking LCOV tooling

I'm working on a Flow dApp written in Cadence and using the testing framework to run unit tests against my contracts. I configured a `CoverageReport` and exported it both as JSON and as LCOV so I could hook it into the standard coverage tooling we already use elsewhere (genhtml, Codecov, Coveralls, etc.).

The reports come out, but the per-file identifiers in them are not file paths — they're Cadence's internal location IDs.

For example, given a `flow.json` like:

```json
{
  "contracts": {
    "FooContract": {
      "source": "contracts/FooContract.cdc",
      "aliases": {
        "testing": "0000000000000007"
      }
    },
    "ApprovalVoting": {
      "source": "contracts/ApprovalVoting.cdc",
      "aliases": {
        "testing": "0000000000000007"
      }
    }
  }
}
```

the LCOV output for those contracts contains records that look roughly like:

```
TN:
SF:A.0000000000000007.FooContract
DA:5,1
DA:6,1
...
end_of_record
TN:
SF:A.0000000000000007.ApprovalVoting
...
```

and the JSON report keys its `coverage` map by those same `A.<address>.<name>` (and `S.<...>` for string locations) identifiers.

The problem is that none of the standard LCOV consumers know what to do with these. `genhtml` expects `SF:` to be an actual source file path so it can read the file and render annotated HTML — it can't find anything called `A.0000000000000007.FooContract` on disk, so the contract just doesn't show up properly in the report. Uploading the LCOV/JSON to Codecov has the same issue: the service can't match these identifiers against the source files in the repo, so coverage doesn't get associated with any file.

What I actually want in those reports is the source path of each contract — e.g. `contracts/FooContract.cdc` — matching what `flow.json` already declares under each contract's `source`. That's the form every downstream coverage tool understands.

I already have this contract-name → source-path mapping in `flow.json` and I don't want to maintain a second copy of it. It would be great if I could pass that mapping into the `CoverageReport` (similar to how I can already configure things like a location filter on it) and have the JSON and LCOV serializations use the mapped source paths in place of the internal location IDs. For any location that isn't in the mapping, falling back to the current behavior is fine.

The new configuration hook I'd expect would be something like `WithLocationMappings(...)` on `CoverageReport`, mirroring the existing `WithLocationFilter`.
