GET request to specific Days instance returns 307 which throws an exception
### Issue Summary
The Days resources is an artifact of running Custom Jobs. When you make a `GET` request to the endpoint, it returns a 307 response with a single key, `redirect_to`, which is a signed url for a compressed JSON file on s3. 

This 307 (Temporary Redirect) causes an exception to be raised here: https://github.com/twilio/twilio-python/blob/master/twilio/base/version.py#L83

Ultimately, this results in the helper class not working and populating the Day instance. Updating the `if` condition on the line linked to above fixes it. It's also worth noting that a simple `curl` of the endpoint, however, succeeds in downloading the file from s3 because it can handle the redirect.

### Code Snippet
```python
days = client.bulkexports.exports('Messages').days.list()

for record in days:
    print(record.friendly_name, record.day, sep=",")
    data = record.fetch()
```

### Exception/Log
```
Test Export,2020-06-01
---------------------------------------------------------------------------
TwilioRestException                       Traceback (most recent call last)
<ipython-input-10-39870118d234> in <module>
      3 for record in days:
      4     print(record.friendly_name, record.day, sep=",")
----> 5     data = record.fetch()

/opt/conda/lib/python3.7/site-packages/twilio/rest/bulkexports/v1/export/day.py in fetch(self)
    356         :rtype: twilio.rest.bulkexports.v1.export.day.DayInstance
    357         """
--> 358         return self._proxy.fetch()
    359 
    360     def __repr__(self):

/opt/conda/lib/python3.7/site-packages/twilio/rest/bulkexports/v1/export/day.py in fetch(self)
    237         :rtype: twilio.rest.bulkexports.v1.export.day.DayInstance
    238         """
--> 239         payload = self._version.fetch(method='GET', uri=self._uri, )
    240 
    241         return DayInstance(

/opt/conda/lib/python3.7/site-packages/twilio/base/version.py in fetch(self, method, uri, params, data, headers, auth, timeout, allow_redirects)
     82 
     83         if response.status_code < 200 or response.status_code >= 300:
---> 84             raise self.exception(method, uri, response, 'Unable to fetch record')
     85 
     86         return json.loads(response.text)

TwilioRestException: HTTP 307 error: Unable to fetch record
```

### Technical details:
* twilio-python version: 6.43.0 
* python version: 3.7.3
