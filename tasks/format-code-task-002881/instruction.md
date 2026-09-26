CreateRepository returns different status codes on subsequent calls
When calling CreateRepository multiple times, the following status codes are returned:

First call: 201 (created)
Second call: 409 (conflict)
Third call: 400 (bad request)
This behavior is unexpected and inconsistent, as it is not clear why subsequent calls to CreateRepository would fail, especially the third call.

All the calls after the first one should check if repository already exists and return a conflict.
