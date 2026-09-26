Add generic type to response headers
### Is your feature request related to a problem? Please describe.

Sometimes APIs use response headers to communicate important metadata, such as rate limit information. At the moment there is no way to type what response headers we expect for a given request, which makes it hard to express/document this.

My use-case is primarily around code generation from openapi specifications, where I'd like to be able to include the declared response headers in the generated code, eg:
```yaml
          headers:
            X-RateLimit-Limit:
              "$ref": "#/components/headers/x-rate-limit-limit"
            X-RateLimit-Remaining:
              "$ref": "#/components/headers/x-rate-limit-remaining"
            X-RateLimit-Reset:
              "$ref": "#/components/headers/x-rate-limit-reset"
```
Should be expressed in output client functions like: https://github.com/mnahkies/openapi-code-generator/blob/main/integration-tests/typescript-axios/src/generated/api.github.com.yaml/client.ts#L1898-L1946

### Describe the solution you'd like

A new generic parameter added to the `AxiosResponse` and associated header types that could be used similar to this:
```typescript
type ResponseBody = {...}

type ResponseHeaders = {
  "x-rate-limit-remaining": string
  "x-rate-limit-used": string
}

function getSomeResource(): Promise<AxiosResponse<ResponseBodyType, ResponseHeaders>> {
...
}
```

Unfortunately there is already a second generic parameter on the `AxiosResponse` so care would be needed to do this in a way that was non-breaking.

### Describe alternatives you've considered

I can probably workaround this on my side, either by moving away from the `AxiosResponse` type, or through an intersection type or similar, but it would be nice if `axios` made it easier to express this kind of information out of the box.

### Additional context/Screenshots

There are a couple of semi-related issues:
- https://github.com/axios/axios/issues/5967
- https://github.com/axios/axios/issues/6677

That would also be nice to see resolved.
