Ability to set OperationName of an AWS API Gateway Method
# Feature Proposal
It would be nice to be able to set OperationName field of an AWS API Gateway Method as shown in the description below.


## Description

<!-- Please use https://forum.serverless.com, StackOverflow or other forums for Q&A -->
<!-- Please answer ALL the question below. Otherwise we probably have to close the issue due to missing information -->

1. What is the use case that should be solved. The more detail you describe this in the easier it is to understand for us.

We  export swagger.yaml from AWS API Gateway resources, and generate client library using [go-swagger](https://github.com/go-swagger/go-swagger) with the exported swagger.yaml. [When exporting to swagger.yaml](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-export-api.html), AWS maps AWS::ApiGateway::Method's OperationName property to Swagger's [OperationId field](https://swagger.io/docs/specification/paths-and-operations/). 

When operationid is not present on swagger.yaml, go-swagger generates function name using combination of method, path, etc, resulting to a very long function name - such as `GetGraphdashboardQuerydsOrganizationIntegrationIDMeasurementMeasureqry` for example.

Since we are unable to set OperationName on serverless.yaml's http event, we are unable to set shorter name to the generated function.

OperationId is also used by other client code generation swagger tool, so this should also be applicable to those tools.

1. **Optional:** If there is additional config how would it look
her
```
      - http:
          path: /integrations/
          method: post
          operationName: CreateIntegration
          documentation:
            summary: Creates a single integration
            description: Creates a single integration
            requestModels:
               "application/json": Integration
            methodResponses:
              - statusCode: '200'
                responseModels:
                  "application/json": Integration
```

Similar or dependent issues:
https://github.com/serverless/serverless/issues/5530
