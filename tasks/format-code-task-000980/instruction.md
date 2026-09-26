The PCAP statistics plugin currently exposes a broker-oriented callback tied to a mutable module global, and consumers cannot obtain a stable, serializable view of the accumulated flow state. Make the flow tracker reusable for offline analysis under the repository's current Python 3 runtime while preserving its existing callback and object APIs.

Network scope and ingestion

- `FlowRecord` must accept an optional `networks` keyword argument. A supplied iterable is copied when the record is created and may contain exact endpoint identifiers plus IPv4 or IPv6 CIDR strings. Exact non-IP identifiers remain valid. When `networks` is omitted or `None`, membership is read from the module-level `network_machines` list at each ingestion so later legacy configuration changes are visible. An explicitly empty iterable means that no endpoints are monitored.
- Add public `FlowRecord.ingest(packet)`. `packet` is a mapping with `src_ip`, `dest_ip`, and `length`. It returns `True` when at least one endpoint is monitored and the packet is recorded, or `False` when both endpoints are outside the configured scope; an ignored packet must not create or change nodes. IPv4 and IPv6 addresses match CIDRs of their own address family.
- A monitored source records one sent packet to the destination, and a monitored destination records one received packet from the source. If two distinct monitored endpoints communicate, each endpoint receives one packet/byte observation. For a monitored self-loop, the node gets one packet/byte observation, while both its sent-to-self and received-from-self counters increment once.

Input and failure semantics

- Endpoint values must be non-empty strings. Packet length must be a non-negative integer; booleans, numeric strings, floats, and negative integers are invalid. A non-mapping packet, a missing required field, or an invalid endpoint or length raises `ValueError`. Validation is atomic: rejected input leaves all accumulated state unchanged.
- Keep the existing `analyze_pcap(ch, method, properties, body, flow)` public callback signature. It must accept a packet mapping directly, a JSON object string, and legacy Python-literal object bytes, pass the decoded packet through the same ingestion rules, and return the same boolean result as `ingest`. Malformed serialization and serialized values that are not mappings raise `ValueError` without changing the flow.

Snapshots and compatibility

- Add `FlowRecord.snapshot(reset=False)`, returning a detached, JSON-serializable dictionary keyed by monitored endpoint. Each value must have exactly `num_packets`, `total_bytes`, `average_packet_length`, `sent_to`, and `received_from`; the two peer fields are dictionaries from endpoint to packet count. Counts and byte totals include all accumulated observations, including those added through the existing `update` API. Mutating a returned snapshot must not affect the tracker.
- With `reset=True`, `snapshot` returns the complete pre-reset snapshot and then empties the accumulated nodes; the same record must remain usable for later ingestion.
- Preserve `FlowRecord.update`, `FlowRecord.get_machine_node`, `MachineNode.num_packets`, `MachineNode.get_avg_packet_len`, and both peer iterator methods. They must remain usable by existing callers under Python 3, including iteration over sent/received peer counts and a `None` result for an unknown node.
