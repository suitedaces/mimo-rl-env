## Feature request: configure VM boot device order from `virt.running` / `virt.defined`

I'm managing libvirt VMs through Salt states (`virt.running` and `virt.defined`) and I can't find a way to control the boot device order of a domain from the state.

My concrete use case: I want to provision a VM that first tries to boot from the network (PXE install) and then falls back to the hard disk, something like:

```yaml
my_vm:
  virt.running:
    - cpu: 2
    - mem: 2048
    - disk_profile: prod
    - disks:
      - name: system
        size: 8192
        pool: default
    - interfaces:
      - name: eth0
        type: network
        source: admin
```

There's no parameter I can pass to make the resulting domain boot from `network` first and `hd` second — the VMs Salt produces always boot from disk only. The `boot` parameter looks like it's only about kernel / initrd / cmdline, not about the `<os><boot dev="..."/></os>` ordering in the libvirt XML.

Could `virt.running` and `virt.defined` (and the underlying module functions used to create / update domains) gain a way to specify the ordered list of boot devices (hd, network, cdrom, fd)? It should also be possible to change the order later on an already-defined VM and have the state actually update the domain definition, not just silently ignore it.

Default behavior (when nothing is specified) should stay the same as today so existing states are not affected.

The new keyword I'd expect on `virt.running` / `virt.defined` (and the underlying `init` / `update` module functions) is something like `boot_dev="network hd"` — a space-separated string of device names — and it should be threaded through to all of them.
