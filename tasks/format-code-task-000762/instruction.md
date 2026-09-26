## `no-ref-siblings` doesn't check referenced files, and results don't tell me which file the violation is in

I have an OpenAPI spec split across several yaml files using `$ref`s to pull in pieces from sibling files (a fairly large API, so keeping it all in one file got unmanageable). I'm running vacuum with the `no-ref-siblings` / `oasRefSiblings` rules enabled.

To sanity-check the linter I deliberately put a violation in one of the referenced files — a `$ref` with a `description` sitting next to it, something like:

```yaml
# components/schemas/Pet.yaml
MyThing:
  $ref: './other.yaml#/components/schemas/Thing'
  description: this shouldn't be here
```

When I lint the root spec, vacuum only flags violations that live in the root file itself. The same kind of violation in any of the `$ref`-pulled files is silently ignored. If I lint that sub-file directly it gets caught, so the rule logic works — it just isn't being applied to the files that get loaded through references.

Related: even for the violations vacuum *does* report, the result doesn't tell me which file the offending node came from. With everything split across files I end up grep-ing through the whole tree to figure out where the flagged `$ref` actually lives. It would be really helpful if the rule result carried the origin file of the node it's complaining about.

Both `no-ref-siblings` (the generic one) and `oasRefSiblings` (the OAS-specific one) behave the same way here.

Could the rule walk the whole set of indexed files rather than just the root one, and surface enough info in each result to identify the source file?
