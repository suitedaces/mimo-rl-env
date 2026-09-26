Feature request: Additional HTTP Error Code Exceptions
### Use case

ref: https://github.com/aws-powertools/powertools-lambda-python/blob/develop/aws_lambda_powertools/event_handler/exceptions.py

I need to handle additional HTTP error codes, specifically 413 (Payload Too Large). I notice that the current exceptions.py only implements a subset of HTTP error codes (400, 401, 404, 500).
While I understand I can extend ServiceError to create my own custom exceptions, this creates inconsistency in my codebase where some errors come from PowerTools and others from my custom definitions.

Are there plans to expand the list of predefined exceptions to cover more HTTP status codes?
What is the rationale behind which HTTP errors are currently implemented vs. those that aren't?

### Solution/User Experience

Add status code

### Alternative solutions

```markdown

```

### Acknowledgment

- [x] This feature request meets [Powertools for AWS Lambda (Python) Tenets](https://docs.powertools.aws.dev/lambda/python/latest/#tenets)
- [x] Should this be considered in other Powertools for AWS Lambda languages? i.e. [Java](https://github.com/aws-powertools/powertools-lambda-java/), [TypeScript](https://github.com/aws-powertools/powertools-lambda-typescript/), and [.NET](https://github.com/aws-powertools/powertools-lambda-dotnet/)
