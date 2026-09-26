add WES API endpoint information to output from `agc context describe`
[//]: #  (Before raising the feature request, please check to see if an existing feature request already exists.)


**Description**

[//]: #  (A short description of the feature you are proposing.)
Add the WES API endpoint url for a context as part of the output from `agc context describe <context-name>`


**Use Case**

[//]: #  (Why do you need this feature?)
Users that write applications that speak GA4GH WES and leverage AGC to manage contexts need a way to retrieve the endpoint to talk to after the context has already been deployed.

**Proposed Solution**

[//]: #  (Please include prototype/workaround/sketch/reference implementation.)
Add a `WESENDPOINT` to the output from `agc context describe <context-name>`

```
$ agc context describe spotCtx
2021-12-10T23:42:58Z �  New version of agc available. Current version is '1.1.1'. The latest version is '1.1.2'
2021-12-10T23:42:58Z �  Describing context 'spotCtx'
CONTEXT 256     spotCtx true    STARTED 
OUTPUTLOCATION  s3://agc-733263974272-us-east-2/project/Demo/userid/pwymingJKP3z/context/spotCtx
WESENDPOINT  https://d1jhugndd0.execute-api.us-east-2.amazonaws.com/prod/ga4gh/wes/v1
```

**Other information**

[//]: #  (detailed explanation, stacktraces, related issues, suggestions how to fix, links for us to have context, eg. associated pull-request, stackoverflow, slack, etc)
