Right now there are four ways to construct an `IPPrefix`:

1. Parsing an string with an IP represented in CIDR notation: `netaddr.ParseIPPrefix("127.0.0.1/8")`
2. Providing the significant bits to an `IP` struct: `netaddr.IPv4(127, 0, 0, 1).Prefix(8)`
3. Working with `IPRange`: `netaddr.ParseRange("127.0.0.0-127.0.0.255").Prefix()` (ignoring error returns)
4. Working with `IPSet`: `ipset.Prefixes()`

I'm working with a kernel API that returns the IP mask itself[^1]. I can turn this into an IPPrefix by first using `net.IPMask` and calling `Size`.

```go
func main() {
	var mask [4]byte
	netmask := make(net.IPMask, net.IPv4len)

	mask = getKernelMask()
	copy(netmask, mask[:])

	bits, _ := netmask.Size()
	ip, _ := netaddr.IPv4(127, 0, 0, 1).Prefix(uint8(bits))

	fmt.Printf("IPPrefix: %s\n", ip)
}
```

Would there be any interest in allowing an `IPPrefix` to be constructed either directly from a netmask representation, or alternatively from a `net.IPMask`?

[^1]: The kernel API returns the netmask for IPv4. For IPv6 they switched to returning the significant bits instead.

I'd expect something like a new `Netmask` method on `IP` taking the raw mask bytes, e.g. `ip.Netmask(maskBytes)`.
