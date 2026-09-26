v2 functions don't support `retry` even though cloud functions gen2 do
<!-- DO NOT DELETE
validate_template=true
template_path=.github/ISSUE_TEMPLATE/bug_report.md
-->

### [REQUIRED] Environment info

<!-- What version of the Firebase CLI (`firebase-tools`) are you using? Note that your issue may already be fixed in the latest versions. The latest version can be found at https://github.com/firebase/firebase-tools/releases -->

<!-- Output of `firebase --version` -->

**firebase-tools:** 11.21.0

<!-- e.g. macOS, Windows, Ubuntu -->

**Platform:** macOS

### [REQUIRED] Test case

<!-- Provide a minimal, complete, and verifiable example (http://stackoverflow.com/help/mcve) -->

```
exports.customeventhandler = onCustomEventPublished(
  {
    eventType: "firebase.extensions.storage-resize-images.v1.complete",
    retry: true,
  },
  (e) => {
    console.log(JSON.stringify(e));
  });
```

### [REQUIRED] Steps to reproduce

<!-- Provide the steps needed to reproduce the issue with the above test case. -->

firebase deploy --only functions

### [REQUIRED] Expected behavior

<!-- What is the expected behavior? -->

Should deploy function with retry policy

### [REQUIRED] Actual behavior

<!-- Run the command with --debug flag, and include the logs below. -->

Shows a warning `Cannot set a retry policy on Cloud Function` and does not set the retry policy.

Warning is coming from here: https://github.com/firebase/firebase-tools/blob/a2b9389928c7586d2bbdfda4f9212bd7fcc88f21/src/gcp/cloudfunctionsv2.ts#L528

`EventTrigger` has `retryPolicy` field, so it should be set when `retry` option is specified.
https://cloud.google.com/functions/docs/reference/rest/v2/projects.locations.functions#eventtrigger
