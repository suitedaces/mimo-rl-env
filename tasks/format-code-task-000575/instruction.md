## Guest can send packets but never receives anything

I'm trying to get networking working in a Linux guest booted by gokvm, using the tap device that gokvm sets up. The outbound direction looks fine — anything the guest sends (ARP, DHCP discover, ping, etc.) shows up on the host's tap interface when I `tcpdump` it.

The reverse direction is broken though. Nothing from the host side ever makes it into the guest:

- DHCP from the guest leaves and the DHCP server on the host replies, but the guest never sees the offer and the request eventually times out, so the interface never gets an address.
- If I assign an address manually and `ping <guest-ip>` from the host, the echo requests are visible on the tap, but the guest doesn't reply. Running `tcpdump` inside the guest on the virtio NIC shows nothing at all — the packets simply never arrive at the guest's NIC.

So in practice the virtio-net device behaves as send-only: the guest can transmit, but nothing the tap delivers ever reaches it. It would be great if gokvm forwarded packets coming in on the tap into the guest's virtio-net device so the NIC actually works as a normal full-duplex interface.

(For symmetry with the existing Tx path, it would be natural to expose the per-packet receive step as a method like `Rx()` on the virtio-net device so it can be driven both from a background thread and from tests.)
