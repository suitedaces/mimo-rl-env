Feature request: Add the ability to access the LambdaContext when using batch processing
### Use case

I'm looking to use the get_remaining_time_in_millis function specifically. In this case, the reason is that my batch size sometimes includes very large items that might time out if they are at the end of the batch. I want to add something to the top of the record_handler that checks the remaining time, and if it's below a threshold it just raises an exception for that record. Then the partial failure mechanism can put the failed items back on the queue.

As it is right now, if the function just times out, everything is put back, not just the failed items.

### Solution/User Experience

Passing the LambdaContext object into the record_handler would be great.

### Alternative solutions

_No response_

### Acknowledgment

- [X] This feature request meets [Lambda Powertools Tenets](https://awslabs.github.io/aws-lambda-powertools-python/latest/#tenets)
- [ ] Should this be considered in other Lambda Powertools languages? i.e. [Java](https://github.com/awslabs/aws-lambda-powertools-java/), [TypeScript](https://github.com/awslabs/aws-lambda-powertools-typescript/)
