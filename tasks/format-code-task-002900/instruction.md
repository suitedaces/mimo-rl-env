## Feature request: shared helper for "regex → matching net interfaces"

We've now got multiple commands that all want the same thing: take a
regular expression (POSIX) from the user, look at the system's netlink
links, and operate on the subset whose names match.

For example, both `cmds/core/dhclient` and `cmds/boot/pxeboot` currently
open-code essentially the same sequence:

```go
ifRE := regexp.MustCompilePOSIX(ifName)

ifnames, err := netlink.LinkList()
if err != nil {
    log.Fatalf("Can't get list of link names: %v", err)
}

var filteredIfs []netlink.Link
for _, iface := range ifnames {
    if ifRE.MatchString(iface.Attrs().Name) {
        filteredIfs = append(filteredIfs, iface)
    }
}

if len(filteredIfs) == 0 {
    log.Fatalf("No interfaces match %s", ifName)
}
```

This pattern has shown up in more than one program now and is likely to
keep coming back (anything that does network setup against a
user-supplied interface pattern). It would be nice to have this as a
reusable helper in the `pkg/dhclient` package so callers can just hand
over the user's RE string and get back the matching `[]netlink.Link`,
and have the existing dhclient / pxeboot call sites use it instead of
their own copies.

Constraints worth keeping:

- The input is a POSIX regex string coming from a user / flag, so a
  malformed pattern shouldn't crash the program — it should surface as
  an error.
- If nothing matches the pattern, that should be treated as an error
  too (the caller asked for interfaces and got none — there's nothing
  useful to do downstream).

A reasonable name for the new helper would be something like
`dhclient.Interfaces(...)`.
