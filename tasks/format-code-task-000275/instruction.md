bug/hardcoded GET request to api.unstructuredapp.io causes timeout behind firewall
**Describe the bug**
There is a hardcoded dummy GET request to api.unstructuredapp.io.  There does not appear to be an easy way to override this, and it also doesn't look necessary. This causes a timeout error behind a firewall and makes the unstructured-client unusable in this environment.  Could this just use the "server_url" parameter for unstructured client? 

https://github.com/Unstructured-IO/unstructured-python-client/blob/18a13093686bca1f97cc061f667fec7db21c489c/src/unstructured_client/_hooks/custom/split_pdf_hook.py#L349

**To Reproduce**
Use the client with personal unstructured-api deployment that is behind a firewall.
```

s= UnstructuredClient(,
        server_url=my_server_url,
        api_key_auth=None
    )
res = s.general.partition(request=req)

```
**Expected behavior**
Request hangs on GET request and will eventually timeout. 

**Environment Info**
unstructured-client=0.26.0
