Support Input and inputPath options in AWS::Events::Rule for schedule events
# This is a Feature Proposal
## Description

At the moment there is no way to pass a predefined input (or an input path) to a schedule event (`AWS::Events::Rule`).

For this purposes Amazon Cloud Formation offers the options `Input` and `InputPath` as documented [here](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html)

e.g.

``` json
{
  "Arn" : "some string",
  "Id" : "some string",
  "Input" : "some string",
  "InputPath" : "some string"
}
```
## Sample use cases
- When you run a lambda with a cron and you want to provide specific custom data to the event (environment dependent variables, configuration attributes, etc.)
## Expected resolution
- Add the support for `Input` and `InputPath` options in `serverless.yml` and then use these options in [plugins/aws/deploy/compile/events/schedule](https://github.com/serverless/serverless/blob/master/lib/plugins/aws/deploy/compile/events/schedule/index.js) to properly populate the [cloud formation template](https://github.com/serverless/serverless/blob/master/lib/plugins/aws/deploy/compile/events/schedule/index.js#L57-L69).
