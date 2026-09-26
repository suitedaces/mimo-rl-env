## Annotations API endpoints don't enforce permissions

I'm wiring up the activity feed to include annotations, and I noticed that the methods on the `Annotations` API class (`createAnnotation`, `deleteAnnotation`, `getAnnotation`, `getAnnotations`) just fire off the HTTP request without first checking whether the caller actually has permission to perform that action on the file.

Compare this with the other feed-related APIs in the codebase — for example `CommentsAPI.getComments` and `AppActivityAPI.getAppActivity` both take the file's permissions as an argument and short-circuit through the error callback (via the shared `checkApiCallValidity` helper on the base class) when the relevant permission is missing. That way the UI gets a consistent error code back instead of us blindly hitting the server and relying on the backend to reject the call.

The annotations endpoints should behave the same way: before making the network request, they should verify that the file (or the annotation itself, in the delete case) grants the appropriate permission, and surface a sensible error through `errorCallback` when it doesn't. The `BoxItem` permission shape will also need to grow whatever new permission flags are needed to express "may this user view annotations on this file" and "may this user create annotations on this file", since those don't exist on `BoxItemPermission` today.

`Feed.fetchAnnotations` (the only current caller inside this repo) should be updated to thread the file's permissions through to the new annotations call so the gate actually runs in practice.

This is purely about parity with how comments / app activity already work — no behavior change for callers that already have the right permissions, just a fast, local rejection (and a proper error code) for callers that don't.
