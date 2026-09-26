SVG Content Type incorrectly encoded as base64
### What version of Hono are you using?

3.11.1

### What runtime/platform is your app running on?

AWS Lambda

### What steps can reproduce the bug?

Return an SVG in a route with

```
c.header('Content-Type', 'image/svg+xml;charset=utf-8');
return c.body(svgString)
```

results in it being base64 encoded.

### What is the expected behavior?

SVG is just text, so it shouldn't need to be encoded before being returned to API Gateway.

PR to fix the regexp in #1788 

### What do you see instead?

It gets encoded, so you cannot render the SVG in a browser.

### Additional information

The relevant code is here: https://github.com/honojs/hono/blame/main/src/adapter/aws-lambda/handler.ts#L264 that was added as part of https://github.com/honojs/hono/pull/1091
