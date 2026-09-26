### NetBox version

v3.2.9

### Python version

3.10

### Steps to Reproduce

1. Create a new VlanGroup with minvid set to 1 and maxvid set to 4094
2. Call the available-vlans endpoint with ?limit=1

### Expected Behavior

Get back one available-vlan object

### Observed Behavior

Get back 4094 available-vlan objects, which in my case causes partial responses to be send which leads to invalid JSON with all associated issues. This only seems to happen with the Guzzle PHP HTTP client, works "fine" in the browser, except for the fact that the request obviously takes ages.

Available-prefix works a bit different and available-ips does seem to support the limit parameter.
