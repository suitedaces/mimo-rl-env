## `acl.present` shows old perms as an octal number, not as `rwx`

When using the `acl.present` state to update an existing ACL, the output's
"old" perms are rendered as a number while "new" perms are the usual
`rwx`-style string. They should be in the same format.

Example state:

```yaml
/root:
  acl.present:
    - acl_type: user
    - acl_name: damian
    - perms: rwx
```

If `damian` already has an ACL on `/root` but with different permissions
(say `rw`), running the state produces something like:

```
        ID: /root
  Function: acl.present
    Result: True
   Comment: Updated permissions for damian
   Changes:
            ----------
            new:
                ----------
                acl_name:
                    damian
                acl_type:
                    user
                perms:
                    rwx
            old:
                ----------
                acl_name:
                    damian
                acl_type:
                    user
                perms:
                    6
```

The `new.perms` is `rwx` but `old.perms` comes out as `6`. Same thing
shows up in the test-mode comment, e.g. `Updated permissions will be
applied for damian: 6 -> rwx`, which is confusing — you can't eyeball
the diff without mentally converting octal back to rwx.

It would be much nicer if `old.perms` was also shown in `rwx` form so
both sides of the change are directly comparable.
