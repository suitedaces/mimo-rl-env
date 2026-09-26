schema.response without a status code throws a cryptic error message
### Prerequisites

- [X] I have written a descriptive issue title
- [X] I have searched existing issues to ensure the bug has not already been reported


### Fastify version

3.29

### Plugin version

_No response_

### Node.js version

16.x

### Operating system

macOS

### Operating system version (i.e. 20.04, 11.3, 10)

12.3.1

### Description

The current response schema definition is:

```
schema: {
  response: {
    $STATUS_CODE: your_schema_here
  }
}
```

I accidentally typed the following:

```
schema: {
  response:  your_schema_here
}
```

This results in an error that is a little cryptic, in my opinion:

```
FastifyError [Error]: Failed building the serialization schema for GET: /meters, due to error schema is invalid: data.properties should be object
```

It seems like this mistake could be captured by fastify, and a better error message could be returned to the user? Obviously the best solution is to RTFM correctly, so I understand if this is deemed not worthwhile :)

### Steps to Reproduce

Pass a schema directly to response, without specifying a status code:

```
app.route({
  url: '/',
  method: 'GET',
  schema: {
    response: {
      type: 'array'
    }
  },
  handler: (req, reply) => {
    reply.send([])
  }
})
```

### Expected Behavior

An error message stating "response schemas should be nested under a response code, e.g { 200: { type: 'object' } }" or similar.
