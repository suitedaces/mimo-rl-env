## Problem Statement

我的 job 里加了个 poststop task 做清理，结果 deploy 一直卡在 running，最后超时变成 unhealthy / failed。但主 task 早就起来了，Consul health check 也是好的。

感觉是那个 poststop task 一直 pending 把整个 deployment 拖住了？它本来就要等主 task 退出才会跑啊，这样我永远没法 deploy 成功。

是我哪里配错了吗，还是说带 poststop 的 job 就没法正常 promote？

## Expected outcomes

- Deployment health with poststop cleanup tasks:
  - A deployment/allocation that includes a `poststop` lifecycle task should be able to become healthy once the normal workload tasks are running and their health checks are passing.
  - A `poststop` lifecycle task that is still pending because the main workload has not exited yet must not by itself keep the deployment in running/pending health until it times out as unhealthy or failed.

- Health semantics for other task outcomes:
  - A task failure should still make the allocation unhealthy.
  - A non-`poststop` task that has already finished when it is expected to participate in allocation health should still make the allocation unhealthy; the poststop cleanup case should not accidentally exempt other lifecycle or normal tasks from health evaluation.
  - A normal or otherwise health-participating task that has not started yet should still prevent the allocation from being reported healthy.

## Implementation notes

- Preserve the existing deployment and allocation health semantics except for the special lifecycle behavior described above.
- The exact internal data structures, helper boundaries, and validation location are up to the implementation, as long as externally observable deployment/allocation health behavior matches the expected outcomes.
