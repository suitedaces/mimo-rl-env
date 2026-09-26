Support checking for arbitrary options on .calls
I'm working on a Cloudflare Worker script that uses arbitrary options on a fetch call (as specified [here](https://developers.cloudflare.com/workers/reference/cloudflare-features/)).

However, I'm unable to test if those options are set correctly because fetch-mock removes them from the options list (as seen [here](https://github.com/wheresrhys/fetch-mock/blob/527d170ecf86b0054d85acfcc7e015b332e78f6f/src/lib/request-utils.js#L41)).

*Example:*

```javascript
function doFetchSomething(url) {
   fetch(url, { cf: { ttl: 30 } })
}

test('should add cf options', () => {
   const fetchMock = require('fetch-mock');
   const url = 'http://some.test.url.io';

   fetchMock.get(url, {});

   doFetchSomething(url);

   expect(fetchMock.calls(filter)[0][1]).toEqual({"cf": {"ttl": 30}, "headers": { "method": "GET"});
});

// Expected: {"cf": {"ttl": 30}, "headers": { "method": "GET"}
// Received: {"headers": { "method": "GET"}
```
