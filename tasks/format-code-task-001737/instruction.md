### Tagging controller silently skips new instances and reports success

I'm running the tagging controller against an EKS cluster. When a node joins, every so often the controller logs a successful tagging, but when I look at the EC2 instance afterward there are no tags on it, and the controller never tries again.

Here's a representative slice from the controller logs for one such node:

```
tags.go:326] Couldn't find resource when trying to tag it hence skipping it, InvalidInstanceID.NotFound: The instance ID 'i-***' does not exist status code: 400, request id: ***
tagging_controller.go:299] Successfully tagged i-*** with map[aws:eks:cluster-name:***]. Labeling the nodes with tagging controller labels now.
tagging_controller.go:305] Successfully labeled node ip-***.compute.internal with map[k8s.io/cloud-provider-aws:***].
```

So what happened is: EC2 didn't know about the instance yet (it was still coming up — `InvalidInstanceID.NotFound`), the tag call effectively did nothing, but the controller treated it as a success and moved on. It also went ahead and labeled the node as if the tagging had happened. The work item never got re-queued, so the instance ends up permanently untagged until something else triggers reconciliation.

I'd expect that if the desired tags aren't actually on the instance, the controller shouldn't claim it tagged it successfully — it should treat that as a failure and let the normal retry / requeue path try again once the instance is visible to EC2.

For the untag direction I think the current behavior is fine: if the instance no longer exists, the desired state (tag absent) is already true, so a no-op success there makes sense. It's specifically the tag-creation side that's lying about success.
