## snap-bootstrap: systemd mount helper has no way to request `noexec` / `nodev`

In preparation for tightening mount options on ubuntu core partitions
(ubuntu-save in particular), I went looking at the systemd-mount helper
in `cmd/snap-bootstrap` (`doSystemdMount` / `systemdMountOptions`) and
noticed there is no way to ask for the partition to be mounted with
`noexec` or `nodev`.

Today `systemdMountOptions` exposes `NoSuid`, `ReadOnly`, `Private`,
`Bind`, etc., but nothing equivalent for the other two hardening
options that are commonly paired with `nosuid` for data partitions
that aren't supposed to hold executables or device nodes. As a result
callers from snap-bootstrap can't express "mount this partition with
noexec,nodev,nosuid" without going around this helper.

It would be good to extend the helper so callers can opt into `noexec`
and `nodev` the same way they opt into `nosuid` today, so the actual
mount invocation ends up passing those options through to
`systemd-mount`.
