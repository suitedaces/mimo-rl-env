Panic is found in log after agent successful initialization [feature/externalnode branch]
**Describe the bug**
Found panic in log after agent initialization for feature/externalnode branch. It doesn't impact the agent running, but we will see the panic in log.
`I0610 07:12:23.519375   14587 agent.go:447] Agent initialized NodeConfig=NodeName: mengdie-k8s0-0, OVSBridge: br-int, PodIPv4CIDR: <nil>, PodIPv6CIDR: <nil>, NodeIPv4: <nil>, NodeIPv6: <nil>, TransportIPv4: <nil>, TransportIPv6: <nil>, Gateway: <nil>, NetworkConfig=&{noEncap  %!v(PANIC=String method: runtime error: index out of range [-1]) {%!v(PANIC=String method: runtime error: index out of range [-1]) }  [] true false}`

It seems that the issue is caused by empty value for trafficEncryptionMode.
In this case, it will return TrafficEncryptionModeInvalid which is -1 since we do not specify default value for it.
`const (
	TrafficEncryptionModeNone TrafficEncryptionModeType = iota
	TrafficEncryptionModeIPSec
	TrafficEncryptionModeWireGuard
	TrafficEncryptionModeInvalid = -1
)`

**To Reproduce**
Run antrea-agent in ExternalNode nodeType

**Expected**
There should be no PANIC in logs since agent initialized successfully.
