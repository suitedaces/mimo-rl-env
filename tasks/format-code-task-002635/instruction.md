Multi-line values in IoT event
<!--
1. If you have a question and not a bug/feature request please ask it at http://forum.serverless.com
2. Please check if an issue already exists so there are no duplicates
3. Check out and follow our Guidelines: https://github.com/serverless/serverless/blob/master/CONTRIBUTING.md
4. Fill out the whole template so we have a good overview on the issue
5. Do not remove any section of the template. If something is not applicable leave it empty but leave it in the Issue
6. Please follow the template, otherwise we'll have to ask you to update it
-->

# This is a Bug Report

Using multi-line values (with yaml >) in an IoT definition results in an 'unexpected token' error.

For bug reports:
* What went wrong?  The following yaml:
```
events:
      - iot:
          description: >
            My multi-
            line value.
          name: enrollPlayer
          sql: >
            SELECT * FROM 'path/#'
            WHERE prop = 'value'
```
complain of an "Unexpected token" when deployed.   Looking at the value of `iotTemplate` in file `serverless/lib/plugins/aws/deploy/compile/events/iot/index.js`, it seems the trailing linefeed is being preserved:
```
           "Description": "My multi- line value.
            ",
            "RuleDisabled": "false",
            "Sql": "SELECT * FROM 'path/#' WHERE prop = 'value'
            ",
```
* What did you expect should have happened?  The multi-line input should not break the ending quote on the next line.
* What was the config you used?
* What stacktrace or error message from your provider did you see?

Similar or dependent issues:
*

* ***Serverless Framework Version you're using***: 1.5.0
* ***Operating System***: OS X 10.12
* ***Stack Trace***:
SyntaxError: Unexpected token 

    at Object.parse (native)
    at /usr/local/lib/node_modules/serverless/lib/plugins/aws/deploy/compile/events/iot/index.js:99:36
    at Array.forEach (native)
    at /usr/local/lib/node_modules/serverless/lib/plugins/aws/deploy/compile/events/iot/index.js:21:28
    at Array.forEach (native)
    at AwsCompileIoTEvents.compileIoTEvents (/usr/local/lib/node_modules/serverless/lib/plugins/aws/deploy/compile/events/iot/index.js:16:47)
    at /usr/local/lib/node_modules/serverless/lib/classes/PluginManager.js:160:50
    at tryCatcher (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/util.js:16:23)
    at Object.gotValue (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/reduce.js:157:18)
    at Object.gotAccum (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/reduce.js:144:25)
    at Object.tryCatcher (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/util.js:16:23)
    at Promise._settlePromiseFromHandler (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:510:31)
    at Promise._settlePromise (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:567:18)
    at Promise._settlePromise0 (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:612:10)
    at Promise._settlePromises (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/promise.js:691:18)
    at Async._drainQueue (/usr/local/lib/node_modules/serverless/node_modules/bluebird/js/release/async.js:138:16)
* ***Provider Error messages***:
  Syntax Error -------------------------------------------
 
     Unexpected token
