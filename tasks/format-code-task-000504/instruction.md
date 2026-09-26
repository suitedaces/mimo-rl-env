## Add support for HTTP API Gateway events

The `events` package in `aws-lambda-go` provides strongly-typed structs for unmarshalling Lambda event payloads, e.g. `APIGatewayProxyRequest` for the REST API Gateway integration. This works great when my Lambda is triggered by a REST API.

However, AWS also offers HTTP API Gateway, which is a separate product with a different (and incompatible) event payload format from the classic REST API Gateway proxy integration. I've configured an HTTP API Gateway in front of my Go Lambda, and when I try to reuse `APIGatewayProxyRequest` to decode the incoming event, the fields don't line up — the payload my Lambda actually receives doesn't match this struct, so a bunch of values come back empty / zero and I lose information that's present in the raw JSON.

Right now my only options are:

1. Write my own struct that mirrors the HTTP API payload shape, or
2. Decode into a `map[string]interface{}` and pull fields out by string keys.

Both feel wrong for a library whose whole job is to give us typed event structs for every supported Lambda trigger.

Could we add a first-class type in `events/apigw.go` (alongside the existing `APIGatewayProxyRequest`) for the HTTP API Gateway event payload, so it can be used the same way:

```go
func handler(ctx context.Context, req events./* HTTP API Gateway type */) (..., error) {
    // ...
}
```

The shape should follow the official AWS docs for the HTTP API Gateway payload format so users can rely on the JSON tags matching what API Gateway actually sends.

The new top-level type I'd expect is something like `APIGatewayV2HTTPRequest` (with a corresponding nested request-context type).
