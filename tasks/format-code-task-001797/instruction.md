[Feature]: Config based "--suppress-warnings" or, more specifically, quiet version mismatch warning
### Description (Problem / Annoyance)

Calling `linode-cli` without `--suppress-warnings` will almost always output a version mismatch warning at the rate this library changes. Using `linode-cli` in scripts requires adding this argument to every call; or get noisy version mismatch messages in logs that are not really helpful for automated processes.

### Proposal

This flag setting should be configurable via `./config/linode-cli` or an ENV VAR (or both ideally). 

- this could be for suppressing all warnings, as it is
- OR, specifically suppressing the version mismatch warning may also be desirable (seems to be the only one that is quite noisy)
- OR both, for example (naming tbd)
    - LINODE_CLI_SUPPRESS_WARNINGS (would suppress all)
    - LINODE_CLI_SUPPRESS_VERSION_WARNING (just the version mismatch)

### References

Here is the [code](https://github.com/linode/linode-cli/blob/cef8240bcd2629e7ea781454f72c0711325ee72a/linodecli/api_request.py#L302) where the warning is generated.

[Example usage](https://github.com/linode/linode-cli/blob/cef8240bcd2629e7ea781454f72c0711325ee72a/linodecli/configuration/__init__.py#L264) currently relying on `sys.argv` instead of `CLI.suppress_warnings` ([here](https://github.com/linode/linode-cli/blob/cef8240bcd2629e7ea781454f72c0711325ee72a/linodecli/cli.py#L36))

### Extra

I could potentially help out with this if it is something that the community/maintainers are open to.

### Potential Usage Example

```
linode-cli account view
The API responded with version 4.173.0, which is newer than the CLI's version of 4.170.2.  Please update the CLI to get access to the newest features.  You can update with a simple `pip3 install --upgrade linode-cli`
┌────────────┬───────────┬──────────────────────┬─────────┬────────────────────┐
│ first_name │ last_name │ email                │ balance │ balance_uninvoiced │
├────────────┼───────────┼──────────────────────┼─────────┼────────────────────┤
│ Larry      │ Linode    │ linode@linode.com    │ 0.0     │ 1,000,000.00       │
└────────────┴───────────┴──────────────────────┴─────────┴────────────────────┘


export LINODE_CLI_SUPPRESS_VERSION_WARNING=true 
linode-cli account view
┌────────────┬───────────┬──────────────────────┬─────────┬────────────────────┐
│ first_name │ last_name │ email                │ balance │ balance_uninvoiced │
├────────────┼───────────┼──────────────────────┼─────────┼────────────────────┤
│ Larry      │ Linode    │ linode@linode.com    │ 0.0     │ 1,000,000.00       │
└────────────┴───────────┴──────────────────────┴─────────┴────────────────────┘
```

Or this could be something like this in `linode-cli` config
```
[DEFAULT]
default-user = DEFAULT
region = us-southeast
type = g6-standard-2
suppress-warnings = false
suppress-version-warning = true
```
