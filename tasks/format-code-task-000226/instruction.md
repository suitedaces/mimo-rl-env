Don't use urlsplit on request path
https://github.com/Pylons/waitress/blob/94e23114bf4e8db9507f3550294037a4804eb053/waitress/parser.py#L257

This leads to things like:

```
>>> from urllib import parse as urlparse
>>> urlparse.urlsplit('//testing/whatever')
SplitResult(scheme='', netloc='testing', path='/whatever', query='', fragment='')
```
Which means we accidentally drop `testing` before sending it on to the WSGI application. Ask me later how I figured that out.

A request such as:

```
GET //testing/whatever HTTP/1.1
```

Is perfectly valid. Non-sensical maybe, but perfectly valid.
