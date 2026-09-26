NSFS | NC | add VIRTUAL_HOSTS to config (currently only in env)
### Environment info
- NooBaa Version: **5.15**
- Platform: **RHEL 8**

### Actual behavior
1. In order to support bucket.hostname instead of path-style we need to let the server set the virtual hostnames it has so that the endpoint could detect the bucket names from the request Host header.
2. Right now this is only available as an env variable - https://github.com/noobaa/noobaa-core/blob/d1bf8c465af745dedbff9d3803ec13da344884ba/src/endpoint/endpoint.js#L103-L108

### Expected behavior
1. This should be added to config.

### Steps to reproduce
1. NA

### More information - Screenshots / Logs / Other output
