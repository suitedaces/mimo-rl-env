With an error like this:

```
Running hack/../test/cmd/builds.sh:81: executing 'oc patch bc/ruby-sample-build -p '{"spec":{"output":{"to":{"name":"origin-ruby-sample:latest"}}}}'' expecting success...
FAILURE after 0.285s: hack/../test/cmd/builds.sh:81: executing 'oc patch bc/ruby-sample-build -p '{"spec":{"output":{"to":{"name":"origin-ruby-sample:latest"}}}}'' expecting success: the command returned the wrong error code
There was no output from the command.
Standard error from the command:
Error from server: unable to find api field in struct BuildConfig for the json field "metadata"
[FAIL] !!!!! Test Failed !!!!
```

Occured in PRs #6335 ([build](https://ci.openshift.redhat.com/jenkins/job/test_pull_requests_origin/8027/consoleFull)), #6409 ([build](https://ci.openshift.redhat.com/jenkins/job/test_pull_requests_origin/7986/consoleFull)).
