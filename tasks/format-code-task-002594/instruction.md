[BUG] Error in exception handling
### Checklist

- [x] I checked the [FAQ section](https://schemathesis.readthedocs.io/en/stable/faq.html#frequently-asked-questions) of the documentation
- [x] I looked for similar issues in the [issue tracker](https://github.com/schemathesis/schemathesis/issues)
- [x] I am using the latest version of Schemathesis

### Describe the bug

I'm getting the following error when the schemathesis gets a network error:

```
An internal error occurred during the test run
schemathesis-schemathesis-1  | 
    Traceback (most recent call last):
      File "/usr/local/lib/python3.10/site-packages/schemathesis/cli/__init__.py", line 1004, in into_event_stream
        yield from runner.from_schema(
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/impl/core.py", line 111, in _generate_events
        for event in self._execute(results, stop_event):
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/impl/solo.py", line 22, in _execute
        for event in self._execute_impl(results):
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/impl/solo.py", line 30, in _execute_impl
        yield from self._run_tests(
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/impl/core.py", line 160, in _run_tests
        for event in run_test(
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/impl/core.py", line 396, in run_test
        yield events.AfterExecution.from_result(
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/events.py", line 158, in from_result
        result=SerializedTestResult.from_test_result(result),
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/serialization.py", line 361, in from_test_result
        errors=[SerializedError.from_exception(error) for error in result.errors],
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/serialization.py", line 361, in <listcomp>
        errors=[SerializedError.from_exception(error) for error in result.errors],
      File "/usr/local/lib/python3.10/site-packages/schemathesis/runner/serialization.py", line 214, in from_exception
        message, extras = extract_requests_exception_details(exception)
      File "/usr/local/lib/python3.10/site-packages/schemathesis/exceptions.py", line 454, in extract_requests_exception_details
        _, reason = exc.args[0].reason.args[0].split(":", maxsplit=1)
    AttributeError: 'ProtocolError' object has no attribute 'reason'
schemathesis-schemathesis-1  | 
Tip: Please consider reporting the traceback above to our issue tracker:
```

It looks like this bug was introduced with the following commit:
https://github.com/schemathesis/schemathesis/commit/8c4fe09c94e65cec9814d8e36fdf379e2810db43

Here is what I got with the `v3.20.0` :
```
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 791, in urlopen
    response = self._make_request(
  File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 537, in _make_request
    response = conn.getresponse()
  File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 461, in getresponse
    httplib_response = super().getresponse()
  File "/usr/local/lib/python3.10/http/client.py", line 1375, in getresponse
    response.begin()
  File "/usr/local/lib/python3.10/http/client.py", line 318, in begin
    version, status, reason = self._read_status()
  File "/usr/local/lib/python3.10/http/client.py", line 287, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response
schemathesis-schemathesis-1  | 
```
