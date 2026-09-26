File variable fallback option fails
<!--
1. If you have a question and not a bug/feature request please ask it at http://forum.serverless.com
2. Please check if an issue already exists so there are no duplicates
3. Check out and follow our Guidelines: https://github.com/serverless/serverless/blob/master/CONTRIBUTING.md
4. Fill out the whole template so we have a good overview on the issue
5. Do not remove any section of the template. If something is not applicable leave it empty but leave it in the Issue
6. Please follow the template, otherwise we'll have to ask you to update it
-->
# This is a Bug Report
## Description
- What went wrong?
  When attempting to use a file variable with a fallback option, and when the file doesn't exist, the fallback is not used and instead I receive an error.
- What did you expect should have happened?
  According to the [documentation](https://serverless.com/framework/docs/guide/serverless-variables#overwriting-variables), it should be possible to have a configuration like: `somevalue: ${file(path):value, self:fallback}` and if a file at `path` does not exist, or if path does exist and there is no `value` within it, fallback to using `self:fallback`)
- What was the config you used?

```
...
provider:
  name: aws
  runtime: nodejs4.3
  region: us-east-1
  iamRoleARN: ${file(.slsconfig):iamRoleARN, self:custom.configuration.iamRoleARN}
custom:
  configuration:
    iamRoleARN: arn:aws:iam::890665980307:role/AA-Lambda-Execution-Role
...
```
- What stacktrace or error message from your provider did you see?
  ENOENT: no such file or directory, open '/path/to/.slsconfig'

Similar or dependent issues:
## Additional Data
- **_Serverless Framework Version you're using**_: 1.0.2
- **_Operating System**_: OSX
- **_Stack Trace**_:
- **_Provider Error messages**_:
