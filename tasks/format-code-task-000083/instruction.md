## ASM policies SDK is missing the Vulnerability Assessment endpoint

I'm using the SDK to script ASM policy management on a BIG-IP. For a given policy I can already get to most of the sub-resources through the lazy attributes — `policy_builder`, `signatures_s`, `blocking_settings`, `history_revisions_s`, etc. — but I can't get to the `vulnerability-assessment` sub-resource.

The endpoint itself is there on the box, e.g.

```
GET /mgmt/tm/asm/policies/<policy-id>/vulnerability-assessment
```

returns the VA config just fine when I hit it directly. But via the SDK there's no corresponding attribute on the policy object, so I have no way to `load()` it / interact with it the way I do with the other policy sub-resources.

Could the Vulnerability Assessment resource be added to the ASM policies module so it works consistently with the other policy sub-resources?
