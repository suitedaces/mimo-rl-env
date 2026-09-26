Django http_request inference can attempt to read request body more than once
First, thank you for adding this feature! It is a welcome addition indeed, and we're looking forward to using it.

After deploying a test version of a Django app using the latest version of the library, we found that making more than one logging call that results in a log line being emitted, within the context of a single HTTP request, results in multiple invocations of `len(request.body)`, where `request` is the same instance of Django's [`HttpRequest`](https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.HttpRequest.body) each time. The `body` attribute is a small wrapper to read the entirety of the request body I/O stream into a bytestring, so evaluating `HttpRequest.body` more than once results in an exception. Here's the relevant note from the Django docs:

> Accessing the `body` attribute after reading the request with either of these I/O stream methods will produce a `RawPostDataException`.

Strictly speaking, the stack trace shown below is from more than one logging call where the second call was from within a middleware, but I believe the same issue exists for any set of one or more calls that occur after `RequestMiddleware` has initially been called and has stashed the current request.

#### Environment details
  - OS type and version: App Engine Standard, Python 3.8
  - Python version: 3.8.6
  - pip version: 20.2.1
  - `google-cloud-logging` version: 2.1.1

#### Steps to reproduce

  1. Add Cloud Logging to a Django application with `google.cloud.logging.Client.setup_logging`
  2. Enable `google.cloud.logging.handlers.middleware.RequestMiddleware` by adding it to the `MIDDLEWARE` list in the Django settings file
  2. In a Django view, add 2 or more logging calls (e.g. `logging.info(...)` such that they will both execute during a request
  3. Run the Django application and send a request that invokes the view

#### Stack trace
```
RawPostDataException: You cannot access body after reading from request's data stream
  File "django/core/handlers/exception.py", line 47, in inner
    response = get_response(request)
  File "app/middleware.py", line 95, in __call__
    logger.info("...")
  File "__init__.py", line 1434, in info
    self._log(INFO, msg, args, **kwargs)
  File "__init__.py", line 1577, in _log
    self.handle(record)
  File "__init__.py", line 1587, in handle
    self.callHandlers(record)
  File "__init__.py", line 1649, in callHandlers
    hdlr.handle(record)
  File "__init__.py", line 950, in handle
    self.emit(record)
  File "/layers/google.python.pip/pip/lib/python3.8/site-packages/google/cloud/logging_v2/handlers/app_engine.py", line 116, in emit
    inferred_http, inferred_trace = get_request_data()
  File "/layers/google.python.pip/pip/lib/python3.8/site-packages/google/cloud/logging_v2/handlers/_helpers.py", line 131, in get_request_data
    http_request, trace_id = checker()
  File "/layers/google.python.pip/pip/lib/python3.8/site-packages/google/cloud/logging_v2/handlers/_helpers.py", line 100, in get_request_data_from_django
    "requestSize": len(request.body),
  File "django/http/request.py", line 316, in body
    raise RawPostDataException("You cannot access body after reading from request's data stream")
