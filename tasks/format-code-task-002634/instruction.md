invoke --data '{ json }' does not parse for Java Lambdas
# This is a (Bug Report / Feature Proposal)
Bug
## Description
The --data argument to 'serverless invoke' is not deserializable in Java lambdas.
For bug reports:
* What went wrong?
Create the sample java lamba
Run 
serverless invoke -f hello --data '{ "key1" : "pwd" }'
( and yes I have tried with all 3 keys )

Result:
```
[0][dlee@z600 newService]$ serverless invoke -f hello  --data '{ "key1" : "pwd" }'
{
    "errorMessage": "An error occurred during JSON parsing",
    "errorType": "java.lang.RuntimeException",
    "stackTrace": [],
    "cause": {
        "errorMessage": "com.fasterxml.jackson.databind.JsonMappingException: Can not instantiate value of type [simple type, class hello.Request] from String value ('{ \"key1\" : \"pwd\" }'); no single-String constructor/factory method\n at [Source: lambdainternal.util.NativeMemoryAsInputStream@dc24521; line: 1, column: 1]",
        "errorType": "java.io.UncheckedIOException",
        "stackTrace": [],
        "cause": {
            "errorMessage": "Can not instantiate value of type [simple type, class hello.Request] from String value ('{ \"key1\" : \"pwd\" }'); no single-String constructor/factory method\n at [Source: lambdainternal.util.NativeMemoryAsInputStream@dc24521; line: 1, column: 1]",
            "errorType": "com.fasterxml.jackson.databind.JsonMappingException",
            "stackTrace": [
                "com.fasterxml.jackson.databind.JsonMappingException.from(JsonMappingException.java:148)",
                "com.fasterxml.jackson.databind.DeserializationContext.mappingException(DeserializationContext.java:875)",
                "com.fasterxml.jackson.databind.deser.ValueInstantiator._createFromStringFallbacks(ValueInstantiator.java:281)",
                "com.fasterxml.jackson.databind.deser.std.StdValueInstantiator.createFromString(StdValueInstantiator.java:284)",
                "com.fasterxml.jackson.databind.deser.BeanDeserializerBase.deserializeFromString(BeanDeserializerBase.java:1176)",
                "com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeOther(BeanDeserializer.java:143)",
                "com.fasterxml.jackson.databind.deser.BeanDeserializer.deserialize(BeanDeserializer.java:134)",
                "com.fasterxml.jackson.databind.ObjectReader._bindAndClose(ObjectReader.java:1511)",
                "com.fasterxml.jackson.databind.ObjectReader.readValue(ObjectReader.java:1102)"
            ]
        }
    }
}
```

OTOH run aws cli

`aws lambda invoke --function-name newService-dev-hello  --payload '{ "key1" : "pwd" }'
`
The payload parses and the result is correct.

Also run


`serverless invoke -f hello --path data.json
`
Where 'data'json' has the same content. 
Result: works as expected.



* What did you expect should have happened?

Payload data pass unchanged so it would deserialize properly

* What was the config you used?

unmodified java8 runtime

* What stacktrace or error message from your provider did you see?
given


* ***Serverless Framework Version you're using***:
1.1.0
* ***Operating System***:
centos7

* ***Stack Trace***:
provided
* ***Provider Error messages***:
provided
