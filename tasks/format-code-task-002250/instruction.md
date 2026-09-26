## API failures silently return an `{'error': ...}` dict instead of raising

When a request to Airtable fails (e.g. wrong table name, bad API key, deleted record), the client currently swallows the failure and hands back a dict that looks like:

```python
{'error': {'code': 404, 'message': '404 Client Error: ...'}}
```

This is really easy to miss. For example:

```python
client = Airtable(base_id, api_key)
response = client.get('TableNameWithATypo')
for record in response['records']:
    ...
```

If the table name is wrong, `get()` doesn't blow up — it returns the error dict above, and then the loop dies with a confusing `KeyError: 'records'` several lines later, far away from the actual problem. Every caller has to remember to manually check `if 'error' in response` after every single call, which nobody actually does.

It also throws away most of the useful information Airtable's API returns on errors. The real response body looks roughly like:

```json
{"error": {"type": "TABLE_NOT_FOUND", "message": "Could not find table ..."}}
```

but the current code reduces it to a generic `requests` HTTPError string, so I can't programmatically tell a "table not found" apart from an "invalid API key" apart from a rate limit.

I'd much rather have the client raise on failed requests so:

1. Mistakes surface immediately at the call site instead of corrupting downstream code.
2. I can `try/except` around calls and inspect what kind of error Airtable actually reported, without having to parse a string.

Could the client raise a proper exception (carrying the type and message the API returned) when a request fails, instead of returning the error-dict shape? I'd expect the new exception class to be something like `AirtableError`, exposed from the package, with the API's `type` and `message` available as attributes on the raised instance.
