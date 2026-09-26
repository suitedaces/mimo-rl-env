## S3 object tagging is not supported by the mock

I'm using `moto` to mock S3 in my test suite. Part of the code under test attaches tags to objects (we use them for downstream lifecycle/cost-allocation logic) and later reads them back. Against real S3 this works fine via boto3's `put_object_tagging` / `get_object_tagging`, but under `@mock_s3` it doesn't behave correctly — there's no working round-trip for object tags.

Minimal repro:

```python
import boto3
from moto import mock_s3

@mock_s3
def test_object_tags():
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="mybucket")
    client.put_object(Bucket="mybucket", Key="myfile", Body=b"hello")

    client.put_object_tagging(
        Bucket="mybucket",
        Key="myfile",
        Tagging={"TagSet": [
            {"Key": "environment", "Value": "staging"},
            {"Key": "team",        "Value": "data"},
        ]},
    )

    resp = client.get_object_tagging(Bucket="mybucket", Key="myfile")
    print(resp["TagSet"])   # expected: the two tags I just put
```

I'd also expect the same to work when tags are supplied inline at upload time via the `Tagging` parameter on `put_object` (i.e. the `x-amz-tagging` header form, like `environment=staging&team=data`), and then retrieved with `get_object_tagging`.

Could object tagging support be added so `put_object_tagging` / `get_object_tagging` (and the inline `Tagging=` on `put_object`) round-trip correctly under `mock_s3`?
