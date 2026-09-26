### wrpcap on sr() results writes wrong timestamps for sent packets

I'm using scapy to do an active probe — build a batch of packets up front, then fire them with `sr()` and save the result for later offline analysis:

```python
pkts = [IP(dst=t)/ICMP() for t in targets]   # built once, ahead of time
ans, unans = sr(pkts, timeout=5)
wrpcap("probe.pcap", ans)
```

When I open `probe.pcap` in wireshark, the timestamps on the **received** replies look fine (they line up with when the answers actually came back). But the timestamps on my **sent** packets are off — they all look like they happened around the same instant, much earlier than the replies, and the inter-packet gaps don't match what I observed on the wire either.

It looks like the sent side is recording the moment the packet object was constructed in Python, not the moment scapy actually put it on the wire. For a small batch built in a list comprehension that's a near-instant burst of identical timestamps, even though `sr()` paced the sends out over several seconds.

This makes the resulting pcap pretty useless for any timing analysis — you can't measure RTT, you can't see send pacing, and the sent/received streams aren't on the same timeline.

Could the sent packets in an `SndRcvList` be written out with the timestamp corresponding to when they were actually sent, so that the pcap reflects what really happened on the wire?
