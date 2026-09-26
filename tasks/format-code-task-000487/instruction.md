## `ToIPDesc` can't parse IPv6 addresses

I'm trying to use `utils.ToIPDesc` with IPv6 peer addresses and it doesn't work. For example:

```go
desc, err := utils.ToIPDesc("::1:9651")
// err != nil  -> "bad ip format"
```

Any IPv6 address goes through this path because `ToIPDesc` looks like it just splits the input on `:` and expects exactly two parts, which is fine for `127.0.0.1:9651` but obviously falls apart the moment the host itself contains colons.

The reverse direction has the same problem. If I build an `IPDesc` with an IPv6 `net.IP` and call `String()` on it, I get something like

```
::1:9651
```

which is ambiguous — you can't tell where the address ends and the port begins, and feeding it back into `ToIPDesc` won't round-trip.

IPv4 still needs to keep working as before (`127.0.0.1:9651` etc.), but `ToIPDesc` / `IPDesc.String()` should handle IPv6 in an unambiguous way so nodes can actually be addressed over v6.
