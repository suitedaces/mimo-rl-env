mergeHeaders unexpected behaviour / type issue
### Environment

`Nuxt 3.12.2 with Nitro 2.9.6`
development mode

### Reproduction

```ts
const headers = new Headers()
if (session.token)
    headers.set("Authorization", `Bearer ${session.token}`)
else
    console.warn(`[PROXY] No token set`)
if (session.domain)
    headers.set("X-Domain", session.domain)
else
    console.warn(`[PROXY] No domain set`)

// note: no 'Authorization' header in the event headers
const mergedHeaders = mergeHeaders(event.headers, headers)

console.log(mergedHeaders.get("Authorization"))
// log: undefined
```

### Describe the bug

The `mergeHeaders` utility won't merge multiple instances of Headers. This is a result of the underlying logic using Object.entries to get a list of key-value pairs which returns an empty array on a Headers instance.

Since `Headers` satisfies the `HeadersInit` type, this should either work, or the types should be changed appropriately.
Once it's clear how we should continue, I will open a PR.

### Additional context

I found this issue when trying to use the proxyRequest / sendProxy utility, basically all of the other utilities depending on mergeHeaders suffer from the type / logic issue and it's not that trivial to find, because you think something is wrong in your code.

### Logs

_No response_
