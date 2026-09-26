Upon comparing the API response of the [get branch protection endpoint](https://docs.github.com/en/rest/branches/branch-protection#get-branch-protection) and the struct implemented here I noticed a few fields missing:
- `required_pull_request_reviews.url string`
- `required_signatures.enabled boolean`
- `required_signature.url string`
- `required_status_checks.contexts []string`
- `required_status_checks.contexts_url string`
- `required_status_checks.url string`
- `url string`

Not sure if the `url` types of fields are left out on purpose but there are some cases when they are implemented (eg. `enforce_admins.url`) so I included them.
