## sysctl.present with test=True bails out when the config file doesn't exist yet

I'm bootstrapping a new minion and using `sysctl.present` to manage a couple of kernel parameters. The target config file (in my case `/etc/sysctl.d/99-salt.conf`) doesn't exist yet — that's expected, the whole point is for Salt to create and populate it on the first apply.

Before applying, I run with `test=True` to see what's about to change:

```yaml
vm.swappiness:
  sysctl.present:
    - value: 20
```

```
salt-call --local state.apply test=True
```

Instead of getting a normal "would be changed to ..." preview, I get:

```
Comment: Sysctl option vm.swappiness might be changed, we failed to check
         config file at /etc/sysctl.d/99-salt.conf. The file is either
         unreadable, or missing.
Result:  None
```

and in the minion log:

```
[ERROR ] Could not open sysctl file
```

That message is misleading — the file isn't unreadable, it just doesn't exist yet, which is a totally normal state for a sysctl-managed config that hasn't been applied for the first time. I'd expect `test=True` in this situation to tell me what changes *would* be made (i.e. that `vm.swappiness = 20` would be added), the same way it would if the file existed but didn't yet contain that key.

Right now there's no way to preview the changes for a fresh host without first manually `touch`ing the config file, which kind of defeats the purpose of running test mode.

This affects both Linux and FreeBSD minions (same behavior on both).
