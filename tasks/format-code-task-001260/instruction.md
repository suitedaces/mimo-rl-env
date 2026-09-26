Error listing Lambda layers after layer deletion
Hi

`lambda.list_layers()` fails if you create a layer and then subsequently delete it

Here's an example illustrating the problem -

```
from moto import mock_lambda, mock_s3

import boto3, unittest, zlib

MyBucket={"name": "my-bucket"}

PyyamlLayer={"name": "pyyaml",
             "bucket": "my-bucket"}

@mock_lambda
@mock_s3
class MockLayerDeleteTest(unittest.TestCase):

    def setup_s3(self, buckets=[MyBucket], layers=[PyyamlLayer]):
        self.s3=boto3.client("s3")
        for bucket in buckets:
            self.s3.create_bucket(Bucket=bucket["name"],
                                  CreateBucketConfiguration={'LocationConstraint': 'EU'})
        for layer in layers:
            s3key="layer-%s.zip" % layer["name"]
            payload=zlib.compress("how now brown cow".encode('utf-8'))
            self.s3.put_object(Bucket=layer["bucket"],
                               Key=s3key,
                               Body=payload,
                               ContentType="application/gzip")
            
    def setUp(self):
        self.setup_s3()
        self.lamda=boto3.client("lambda")
            
    def test_create_delete_list_layer(self, bucket=MyBucket, layer=PyyamlLayer):
        s3key="layer-%s.zip" % layer["name"]
        print ("--- creating layer ---")
        resp=self.lamda.publish_layer_version(LayerName=layer["name"],
                                              Content={"S3Bucket": bucket["name"],
                                                       "S3Key": s3key})
        layerarn=resp["LayerVersionArn"]
        layerversion=int(layerarn.split(":")[-1])
        print (self.lamda.list_layers()) # <- WORKS FINE HERE
        print ("--- deleting layer ---")
        self.lamda.delete_layer_version(LayerName=layer["name"],
                                        VersionNumber=layerversion)
        print (self.lamda.list_layers()) # <- FAILS HERE
    
    def teardown_s3(self, buckets=[MyBucket]):
        def empty_bucket(s3, bucket):            
            struct=s3.list_objects(Bucket=bucket["name"])
            if "Contents" in struct:
                for obj in struct["Contents"]:
                    # print ("deleting %s" % obj["Key"])
                    s3.delete_object(Bucket=bucket["name"],
                                     Key=obj["Key"])
        def delete_bucket(s3, bucket):
            s3.delete_bucket(Bucket=bucket["name"])
        for bucket in buckets:
            empty_bucket(self.s3, bucket)
            delete_bucket(self.s3, bucket)

    def tearDown(self):
        self.teardown_s3()

if __name__=="__main__":
    unittest.main()
```

And here's what happens when you run it -

```
(env) jhw@Justins-Air layman2 % python dev/mock_layer_delete_test.py
--- creating layer ---
{'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {}, 'RetryAttempts': 0}, 'Layers': [{'LayerName': 'pyyaml', 'LayerArn': 'arn:aws:lambda:eu-west-1:123456789012:layer:pyyaml', 'LatestMatchingVersion': {'LayerVersionArn': 'arn:aws:lambda:eu-west-1:123456789012:layer:pyyaml:1', 'Version': 1, 'Description': '', 'CreatedDate': '2022-08-03 14:22:07', 'CompatibleRuntimes': [], 'LicenseInfo': '', 'CompatibleArchitectures': []}}]}
--- deleting layer ---
E
======================================================================
ERROR: test_create_delete_list_layer (__main__.MockLayerDeleteTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/core/models.py", line 120, in wrapper
    result = func(*args, **kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/core/models.py", line 120, in wrapper
    result = func(*args, **kwargs)
  File "dev/mock_layer_delete_test.py", line 43, in test_create_delete_list_layer
    print (self.lamda.list_layers()) # <- FAILS HERE
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/client.py", line 508, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/client.py", line 898, in _make_api_call
    http, parsed_response = self._make_request(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/client.py", line 921, in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/endpoint.py", line 119, in make_request
    return self._send_request(request_dict, operation_model)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/endpoint.py", line 202, in _send_request
    while self._needs_retry(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/endpoint.py", line 354, in _needs_retry
    responses = self._event_emitter.emit(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/hooks.py", line 412, in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/hooks.py", line 256, in emit
    return self._emit(event_name, kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/hooks.py", line 239, in _emit
    response = handler(**kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/retryhandler.py", line 207, in __call__
    if self._checker(**checker_kwargs):
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/retryhandler.py", line 284, in __call__
    should_retry = self._should_retry(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/retryhandler.py", line 307, in _should_retry
    return self._checker(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/retryhandler.py", line 363, in __call__
    checker_response = checker(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/retryhandler.py", line 247, in __call__
    return self._check_caught_exception(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/retryhandler.py", line 416, in _check_caught_exception
    raise caught_exception
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/endpoint.py", line 278, in _do_get_response
    responses = self._event_emitter.emit(event_name, request=request)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/hooks.py", line 412, in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/hooks.py", line 256, in emit
    return self._emit(event_name, kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/botocore/hooks.py", line 239, in _emit
    response = handler(**kwargs)
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/core/botocore_stubber.py", line 55, in __call__
    status, headers, body = response_callback(
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/awslambda/responses.py", line 80, in list_layers
    return self._list_layers()
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/awslambda/responses.py", line 461, in _list_layers
    layers = self.lambda_backend.list_layers()
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/awslambda/models.py", line 1434, in list_layers
    return self._layers.list_layers()
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/awslambda/models.py", line 1245, in list_layers
    return [layer.to_dict() for layer in self._layers.values()]
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/awslambda/models.py", line 1245, in <listcomp>
    return [layer.to_dict() for layer in self._layers.values()]
  File "/Users/jhw/work/layman2/env/lib/python3.8/site-packages/moto/awslambda/models.py", line 370, in to_dict
    "LatestMatchingVersion": self.layer_versions[
KeyError: '1'

----------------------------------------------------------------------
Ran 1 test in 0.264s

FAILED (errors=1)
```

I'm using the latest version of `moto` - `3.1.16`

Rgds :)
