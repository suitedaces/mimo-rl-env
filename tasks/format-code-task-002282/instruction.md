## `iter_bucket` doesn't let me choose which AWS credentials/profile to use

I'm using `smart_open.s3.iter_bucket` to bulk-download keys from a bucket that I can only access via a specific AWS profile (not the default one in `~/.aws/credentials`). For the regular `smart_open.open(...)` path I can build a `boto3.Session(profile_name=...)` and pass it in, so that works fine.

But with `iter_bucket` there's no equivalent — it always ends up using the default boto3 session, so it tries to authenticate as the wrong identity and I get access-denied errors against a bucket I can otherwise read just fine.

Minimal example of what I'd like to be able to do:

```python
from smart_open.s3 import iter_bucket

# this bucket is only accessible under a specific profile / region
for key, content in iter_bucket(
        'my-restricted-bucket',
        prefix='foo/',
        profile_name='my-profile',
        region_name='us-west-2'):
    ...
```

Right now those extra session-level arguments have nowhere to go — `iter_bucket` doesn't accept them, and the worker processes it spawns internally each construct their own default session too, so even monkey-patching the outer call wouldn't help.

Could `iter_bucket` be extended so I can tell it which AWS credentials/profile/region to use when talking to S3? Ideally it would also propagate that down to whatever it does in the worker processes, so the listing call and the per-key download call both use the same credentials.
