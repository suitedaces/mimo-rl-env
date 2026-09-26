Update Lambda configuration on deploy function
## This is a Feature Proposal

### Description

When deploying a single function with `sls deploy function -f myFunction`, I propose the ability to update the configuration of the Lambda function. Currently the only choices are:
a) update only the code bundle; or 
b) do a full `serverless deploy` which touches CloudFormation and deploys all available changes.

Lambda function configurations can be updated directly using `AWS.Lambda::updateFunctionConfiguration`. CloudFormation would receive the change on the next full deploy (note: changes would be overwritten in this scenario by a manual CF deploy outside of Serverless).

Common use cases for this include updating environment variables while developing a new function, or testing different RAM settings for performance w/o wanting to deploy other functions or multitask in the AWS Console.

### Proposed syntax
This feature should be a simple option/flag to retain backwards compatibility.
`sls deploy function -f myFunction --update-config

Note: I am willing and able to create a PR for this.
