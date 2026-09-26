vcsim doesn't support SuspendVM / ResetVM

I'm using `vcsim` to integration-test some tooling we have around lifecycle operations on VMs. PowerOn and PowerOff against a simulated VM work fine, but as soon as my code calls Suspend or Reset on a VM it falls over against the simulator (it works against a real vCenter).

Minimal repro with govc against a vcsim endpoint:

```
$ vcsim &
$ export GOVC_URL=...   # point at vcsim
$ govc vm.power -on  /DC0/vm/DC0_H0_VM0    # ok
$ govc vm.power -off /DC0/vm/DC0_H0_VM0    # ok
$ govc vm.power -on  /DC0/vm/DC0_H0_VM0
$ govc vm.power -suspend /DC0/vm/DC0_H0_VM0   # fails against vcsim
$ govc vm.power -reset   /DC0/vm/DC0_H0_VM0   # fails against vcsim
```

The same calls work against a real vCenter and the VM ends up suspended / reset respectively. It'd be great if vcsim could handle these two power operations as well so we don't have to special-case the simulator in our tests.

It would also be nice if the simulated VM produced the same kinds of state-transition events as the real product does for these operations, since some of our tests watch the event stream to know when a transition has occurred.
