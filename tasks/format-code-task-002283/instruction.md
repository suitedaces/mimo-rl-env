Probably avoidable fatal S3 race condition
#### Problem description

When using `s3.iter_bucket` from my Lambda, I observed the following problem.

A user on my system was deleting an object (valid use case). While that user was deleting it, unrelated to it, `smart_open.s3.iter_bucket` kicked off. Inside that function, the key iterator is created, and then a download is started for each key. The key (of the object about to be deleted) showed up in the result. Once it was time to download the object, it was no longer there, and a 404 was thrown, which proved fatal and an exception was thrown.

While this may seem like a fluke,

a) it was on a system with very little user activity.
b) S3's list operation is (iirc) not strongly consistent and may for a certain duration return keys that have already been deleted.

So it may be more common than it seems. I think that it would be reasonable for `iter_bucket` to skip objects that return a 404 during their download (ie: catch the error and suppress it), and carry on iterating. I think `iter_bucket` would still fulfill its duty this way.

#### Steps/code to reproduce the problem

The code:

```python
def get_all_metadata() -> list[dict]:
    bucket = get_s3_bucket()
    prefix = f"{get_s3_path()}/"
    accept_key = lambda key: key.endswith(get_metadata_ext())

    # Not explicitly setting this property to False will cause an error in the Lambda runtime when
    # running iter_bucket. This is a known issue, but it doesn't look like it will be resolved:
    # https://github.com/RaRe-Technologies/smart_open/issues/605

    smart_open.concurrency._MULTIPROCESSING = False

    return [
        json.loads(content)
        for key, content in smart_open.s3.iter_bucket(
            bucket, prefix=prefix, accept_key=accept_key
        )
    ]
```

The error:

```
[ERROR] ClientError: An error occurred (404) when calling the HeadObject operation: Not Found
Traceback (most recent call last):
  File "/var/task/lambdas/filemanager/list.py", line 20, in handler
    metadata_list = filemanager.get_all_metadata()
  File "/var/task/lambdas/lib/filemanager.py", line 78, in get_all_metadata
    return [
  File "/var/task/lambdas/lib/filemanager.py", line 78, in <listcomp>
    return [
  File "/var/task/smart_open/s3.py", line 1192, in iter_bucket
    for key_no, (key, content) in enumerate(result_iterator):
  File "/var/task/smart_open/concurrency.py", line 58, in imap_unordered
    yield future.result()
  File "/var/lang/lib/python3.9/concurrent/futures/_base.py", line 439, in result
    return self.__get_result()
  File "/var/lang/lib/python3.9/concurrent/futures/_base.py", line 391, in __get_result
    raise self._exception
  File "/var/lang/lib/python3.9/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/var/task/smart_open/s3.py", line 1254, in _download_key
    content_bytes = _download_fileobj(bucket, key_name)
  File "/var/task/smart_open/s3.py", line 1271, in _download_fileobj
    bucket.download_fileobj(key_name, buf)
  File "/var/runtime/boto3/s3/inject.py", line 719, in bucket_download_fileobj
    return self.meta.client.download_fileobj(
  File "/var/runtime/boto3/s3/inject.py", line 679, in download_fileobj
    return future.result()
  File "/var/runtime/s3transfer/futures.py", line 103, in result
    return self._coordinator.result()
  File "/var/runtime/s3transfer/futures.py", line 266, in result
    raise self._exception
  File "/var/runtime/s3transfer/tasks.py", line 269, in _main
    self._submit(transfer_future=transfer_future, **kwargs)
  File "/var/runtime/s3transfer/download.py", line 354, in _submit
    response = client.head_object(
  File "/var/runtime/botocore/client.py", line 391, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/var/runtime/botocore/client.py", line 719, in _make_api_call
    raise error_class(parsed_response, operation_name)
```

#### Versions

This is running on:

* AWS Lambda
* Intel
* Python 3.9
* smart_open 5.2.1

#### Checklist

Before you create the issue, please make sure you have:

- [x] Described the problem clearly
- [x] Provided a minimal reproducible example, including any required data
- [x] Provided the version numbers of the relevant software
