raise_for_request should not be used for non-successful response
Hi there,

I'm wondering why you elected to use `response.raise_for_status()` after receiving the response - https://github.com/okigan/awscurl/blob/184d7735b57d5c71f75f52a85cc8c8909226b6d5/awscurl/awscurl.py#L537

Would it not make more sense to return an exit code that is either 0 for a successful request or non-zero for a non-successful request?

This would mean tools such as jq etc could still parse the response without the Python traceback interfering where a non-successful status code may still be anticipated.

Happy to open a PR if it makes sense.
