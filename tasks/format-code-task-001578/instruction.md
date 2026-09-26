## cloud-init fails on AlmaLinux/RHEL: `ValueError: Address default is not a valid ip address`

I'm using cluster-api-provider-proxmox to bring up nodes from an AlmaLinux 9 cloud image template. On Ubuntu 22.04 templates everything is fine, but on RPM-based distros the VM comes up without network — `cloud-init` blows up in the `init-local` stage and never applies the network config.

Here's the relevant tail from `/var/log/cloud-init.log` on the failing AlmaLinux VM:

```
2023-12-14 13:24:13,681 - stages.py[INFO]: Applying network configuration from ds bringup=False: {'version': 2, 'renderer': 'networkd', 'ethernets': {'eth0': {'match': {'macaddress': '9E:88:BA:6F:CC:1A'}, 'dhcp4': 'no', 'addresses': ['192.168.69.111/24'], 'routes': [{'to': 'default', 'via': '192.168.69.1'}], 'nameservers': {'addresses': ['8.8.8.8', '8.8.4.4']}}}}

2023-12-14 13:24:13,684 - util.py[DEBUG]: failed stage init-local
Traceback (most recent call last):
  ...
  File "/usr/lib/python3.9/site-packages/cloudinit/net/network_state.py", line 1009, in _normalize_net_keys
    raise ValueError(f"Address {addr} is not a valid ip address")
ValueError: Address default is not a valid ip address
```

So the network-config that capmox generates and feeds into cloud-init contains a route entry that the cloud-init shipped on AlmaLinux/RHEL 9 refuses to accept — it expects the route destination to be a valid IP/CIDR.

The Ubuntu 22.04 cloud-init happens to accept it, which is why this only shows up once you try to use a non-Debian-family image.

Could the rendered network-config be adjusted so that the default-route entries are expressed in a form that cloud-init accepts on both Ubuntu and RPM-based distros? Needs to cover both IPv4 and IPv6 gateways.
