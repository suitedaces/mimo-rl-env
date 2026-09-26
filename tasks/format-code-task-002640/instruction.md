Configuration error at 'functions.hello': unrecognized property 'custom'
After serverless framework 2.6.0 version, not able to giving custom properties during function definition. https://github.com/serverless/serverless/pull/8385/commits/97b7a486d2dcc470d2820ea098d1622073dd8080 this change may have caused the problem.
```yaml
functions:
  hello:
    handler: handler.hello
    custom:
      thundra:
        disable: true
```
<details>
<summary><code>serverless.yml</code></summary>

```yaml
service: serverlessnode10example

frameworkVersion: '2'

configValidationMode: error

provider:
  name: aws
  runtime: nodejs10.x
  stage: dev
  region: eu-west-1

functions:
  hello:
    handler: handler.hello
    custom:
      thundra:
        disable: true

plugins:  
  - serverless-plugin-thundra
```

</details>

<details>
<summary><b><code>sls deploy</code> output</b></summary>

```
Serverless Error ---------------------------------------
 
  Configuration error at 'functions.hello': unrecognized property 'custom'
 
  Get Support --------------------------------------------
     Docs:          docs.serverless.com
     Bugs:          github.com/serverless/serverless/issues
     Issues:        forum.serverless.com
 
  Your Environment Information ---------------------------
     Operating System:          darwin
     Node Version:              12.18.4
     Framework Version:         2.8.0
     Plugin Version:            4.1.1
     SDK Version:               2.3.2
     Components Version:        3.2.4
```

</details>

<b>Installed version</b>

```
Framework Core: 2.8.0
Plugin: 4.1.1
SDK: 2.3.2
Components: 3.2.4
```
