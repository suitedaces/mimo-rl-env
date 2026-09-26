OpenAPI formats not supported?
I'm a bit confused regarding schema formats. 
According to the [Swagger OpenAPI 3.0 page](https://swagger.io/specification/), formats such as `int32`, `byte` etc are supported by OpenAPI 3.0:
![Skärmbild från 2020-05-26 11-43-51](https://user-images.githubusercontent.com/9608258/82886185-75bbf200-9f46-11ea-97ba-2d6b28f6c323.png)

However, I cannot find these in the [OpenAPI 3.0 schema itself at github](https://github.com/OAI/OpenAPI-Specification/blob/master/schemas/v3.0/schema.yaml).

Anyway, whenever my definitions make use of `format` for schemas, I get warnings from openapi-backend. Consider the following:

```
paths:
  /foo:
    post:
      operationId: foo
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                foo:
                  type: integer
                  format: int32
                bar:
                  type: string
                  format: byte         
```

Making a request to this operation renders this:

```
unknown format "int32" ignored in schema at path #/properties/requestBody/properties/foo
unknown format "byte" ignored in schema at path #/properties/requestBody/properties/bar
```

Should these formats be supported or ignored?
