Can't deploy with master branch: "Cannot read property 'endsWith' of null"
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

Installed from master branch (needed to pull in https://github.com/serverless/serverless/pull/2014), and `serverless deploy` no longer works.  I get the error "Cannot read property 'endsWith' of null".

This happens with full Admin AWS credentials on the hello-world project created by `serverless create --template aws-nodejs`

For bug reports:
- What went wrong?
- What did you expect should have happened?
- What was the config you used?
- What stacktrace or error message from your provider did you see?
## Additional Data
- **_Serverless Framework Version you're using**_: 1.0.2
- **_Operating System**_: Ubuntu 14
- **_Stack Trace**_: below
- **_Provider Error messages**_: none

``` bash
$ SLS_DEBUG=true serverless deploy -v

Serverless: Packaging service...
Serverless: Removing old service versions...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading service .zip file to S3...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...

  Serverless Error ---------------------------------------

     Cannot read property 'endsWith' of null

  Stack Trace --------------------------------------------

ServerlessError: Cannot read property 'endsWith' of null
    at sdk.request.then.catch (/home/ubuntu/.npm-global/lib/node_modules/serverless/lib/plugins/aws/lib/monitorStack.js:97:26)
    at tryCatcher (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/util.js:16:23)
    at Promise._settlePromiseFromHandler (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:510:31)
    at Promise._settlePromise (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:567:18)
    at Promise._settlePromise0 (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:612:10)
    at Promise._settlePromises (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:687:18)
    at Async._drainQueue (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/async.js:138:16)
    at Async._drainQueues (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/async.js:148:10)
    at Immediate.Async.drainQueues (/home/ubuntu/.npm-global/lib/node_modules/serverless/node_modules/bluebird/js/release/async.js:17:14)
    at runCallback (timers.js:574:20)
    at tryOnImmediate (timers.js:554:5)
    at processImmediate [as _immediateCallback] (timers.js:533:5)

  Get Support --------------------------------------------
     Docs:          docs.serverless.com
     Bugs:          github.com/serverless/serverless/issues

  Your Environment Infomation -----------------------------
     OS:                 linux
     Node Version:       6.7.0
     Serverless Version: 1.0.2
```
