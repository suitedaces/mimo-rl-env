## yumpkg: a couple of rough edges hit while using `pkg.group_install` / `pkg.download`

I'm running Salt 3006 on RHEL-family minions (Py3) and ran into two issues with the `pkg` module (yumpkg) that I think are worth fixing together.

### 1. `pkg.group_install` fails on some package groups

I'm trying to install a package group:

```
salt '*' pkg.group_install "Development Tools"
```

For most groups this works, but for some it fails — the underlying yum/dnf call complains and nothing gets installed. After staring at the resolved package list for the group, it looks like some packages show up more than once in what `group_install` ends up handing off to `install`. It feels like the group resolution can legitimately produce the same package via different paths (mandatory + default, or via `include`), and `group_install` just passes the list through as-is.

I'd expect `pkg.group_install` to install the union of packages in the group — duplicates in the resolved list shouldn't make the whole call blow up.

### 2. `pkg.download` on a minion without `yumdownloader` is confusing

On a minion where `yumdownloader` isn't installed (it ships in `yum-utils` / `dnf-utils` and isn't always there by default), calling

```
salt 'minion' pkg.download httpd
```

doesn't behave like a normal "command failed" — instead it looks as if `pkg.download` itself isn't a thing on that minion, which had me chasing the wrong problem for a while (checking grains, virtual module detection, etc.) before I figured out the real reason was just a missing helper binary.

If the prerequisite tool isn't on the system, I'd expect `pkg.download` to still exist and just fail loudly with a clear message saying that's the reason, the same way other `pkg` functions do when they can't proceed.

---

Both are on the same module so I'm filing them together. Happy to test fixes on RHEL 8 / 9 and Rocky.
