Allow for the removal of default request mapping templates
Currently [default request mapping templates are created ](https://github.com/serverless/serverless/blob/v1.58.0/lib/plugins/aws/package/compile/events/apiGateway/lib/method/integration.js#L189) both for application/json and application/x-www-form-urlencoded. There does not appear to be a simple method for overriding this default. In our application we only support the application/json content type however application/x-www-form-urlencoded is being automatically created even though it is not supported by our application. Even worse, when generating swagger documentation via the AWS API Gateway this forces us advertise that we consume both:

"consumes": [
          "application/json",
          "application/x-www-form-urlencoded"
        ],

IMO, there really should be a way of overriding defaults in any application. If you can suggest any workaround to this it would be great
