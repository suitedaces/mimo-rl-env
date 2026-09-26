### No way to abort an in-progress chunked upload from `ChunkedUploader`

I'm using the automatic chunked uploader to push large video files to Box:

```python
test_file_path = '/path/to/large_file.mp4'
content_stream = open(test_file_path, 'rb')
total_size = os.stat(test_file_path).st_size
chunked_uploader = client.upload_session('56781').get_chunked_uploader_for_stream(content_stream, total_size)
uploaded_file = chunked_uploader.start()
```

Occasionally `start()` blows up partway through (flaky network, the connection drops on one of the parts, etc.). At that point I've already uploaded a bunch of parts on the server side and I'd like to cleanly cancel the whole thing so I can start over with a fresh session.

The problem is the `ChunkedUploader` object doesn't expose any way to do that. I can see that `UploadSession` itself has an abort, and the manual chunked-upload flow documents using it, but when you go through the automatic uploader you're holding a `ChunkedUploader` and there's no equivalent on it — so wrapping `start()` in a try/except doesn't really help me recover, because I have nothing to call in the `except` branch to tear the session down.

It would be great if `ChunkedUploader` itself supported cancelling — something I can call from an `except` clause to abort the upload and clean up the parts that were already uploaded. Ideally after that the uploader instance is "dead" and trying to resume/start it again would fail loudly rather than do something undefined, so callers are pushed toward creating a fresh upload session.
