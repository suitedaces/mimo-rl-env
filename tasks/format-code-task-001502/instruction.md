## Brother printer: zeroconf discovery reports wrong error and ignores broadcast model info

I have a Brother printer at home that Home Assistant auto-discovers via mDNS. The integrations page pops up the usual "Discovered: Brother Printer" card. When I click "Configure" to add it, the flow aborts immediately with **"Failed to connect to the device"**.

The thing is, the printer is fine — I can ping it, open its web admin page in the browser, print to it from my laptop, etc. So the "cannot connect" message isn't really telling me what's wrong.

Out of frustration I went the manual route instead: Integrations → Add Integration → Brother Printer → typed in the IP. That flow gave me a much more useful message saying the model isn't supported. So the printer is reachable, it's just not a model the integration handles — but only the manual path tells me that. The zeroconf-discovered path collapses every failure into "cannot connect", which sent me down a totally wrong debugging path (checking firewalls, SNMP being blocked, etc.).

Two things I'd expect from the discovery flow:

1. It should distinguish between "I can't reach the printer" and "I reached it but the model isn't supported", the same way the manual step does. Right now both look identical to the user, and the wrong one is shown for an unsupported model.

2. The zeroconf announcement from the printer actually contains the model/product name in its TXT properties (you can see it with `avahi-browse -r` etc.). It seems wasteful for HA to throw that information away and rely solely on probing the device afterwards — if the broadcast already tells us what model it is, the integration could use that during setup instead of (or in addition to) querying it separately.

Could the zeroconf discovery path be brought in line with the manual flow on error reporting, and also make use of the model info that the printer is already advertising?
