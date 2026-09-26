In my code I use the following pattern
```
conn, err := dbus.SystemBus()
if err != nil {
	return nil, err
}
defer conn.Close()
```

And in the first function it works great, but the second function fails with error "dbus: connection closed by user". If I remove `defer conn.Close()` the both functions work great.

It would also be helpful to have a way to query whether a connection is still alive, e.g. something like `conn.Connected()`.
