Credential Script not called correctly from Defaults section
### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please let us know in a comment
<!-- Thank you for keeping this note for the community -->


### Problem

If I put "credential_script" configuration in the Defaults section of the harvest.yml, the script is called only with username parameter, not with address. If it is in the Pollers section it works correctly.

Also I find the wording of the feature documentation a bit misleading. 
> Harvest will call the script with two arguments via standard in

That made me think the script is called like this `echo "hostname username" | get_pass`



### Configuration

```text
Admin:
  httpsd:
    listen: 127.0.0.1:8887

Tools:
  grafana_api_token: abc
  autosupport_disabled: true

Exporters:
  prometheus:
    exporter: Prometheus
    local_http_addr: localhost
    port_range: 12990-13013
    sort_labels: true

Defaults:
  collectors:
    - Zapi
    - ZapiPerf

  exporters:
    - prometheus

  auth_style: basic_auth
  username: foo_ontap

  credentials_script:
    path: ./get_pass
    schedule: 12h
    timeout: 10s
    
Pollers:
  ontap1:
    datacenter: DC1
    addr: ontap1.local
    
  ontap2:
    datacenter: DC1
    addr: ontap2.local
    
  StorageGrid1:
    datacenter: DC1
    addr: storagegrid1.local
    username: foo
    password: bar
    collectors:
      - StorageGrid
```


### Poller

all

### Version

harvest version 23.05.0-1 (commit 6f74c7a5) (build date 2023-05-03T08:08:46-0400) linux/amd64

### Poller logs

_No response_

### OS and platform

Red Hat Enterprise Linux release 8.7 (Ootpa)

### ONTAP or StorageGRID version

9.11.1P8

### Additional Context

_No response_

### References

_No response_
