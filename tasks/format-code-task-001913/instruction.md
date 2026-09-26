### Missing `-A` switch for Dedicated Admin Connection

The original `sqlcmd` utility supports an `-A` switch that opens a Dedicated Administrator Connection (DAC) to SQL Server (see the [sqlcmd reference](https://learn.microsoft.com/sql/tools/sqlcmd-utility)). This is what I rely on to log into a server when normal connections are blocked or unresponsive — for example, when the server is starved of worker threads and I need to get in to diagnose what's going on.

I tried doing the same thing with `go-sqlcmd`:

```
sqlcmd -S myserver -U sa -A -Q "SELECT @@SPID"
```

but `-A` isn't recognized as a flag, and there doesn't seem to be any equivalent long-form flag either. As far as I can tell there's currently no way to ask `go-sqlcmd` to connect over the DAC endpoint.

Could `-A` be added so `go-sqlcmd` can be used as a drop-in replacement for the classic `sqlcmd` when DBAs need an admin connection? It should behave the same as the original — when the switch is set, the connection should be made over the dedicated admin endpoint instead of the regular one.
