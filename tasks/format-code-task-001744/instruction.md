Scheduler should return specific errors for affinity predicates
<!-- This form is for bug reports and feature requests ONLY! 

If you're looking for help check [Stack Overflow](https://stackoverflow.com/questions/tagged/kubernetes) and the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/).
-->

**Is this a BUG REPORT or FEATURE REQUEST?**: FEATURE REQUEST

> Uncomment only one, leave it on its own line: 
>
> /kind bug

/kind feature

Today predicate functions return `ErrPodAffinityNotMatch` for these three cases: 1) pod affinity rules failed, 2) pod anti-affinity rules failed, 3) pod violated other pods anti-affinity rules. We should return a specific error in each one of these three cases. Separate error codes help when processing these failures in other parts of the code. For example, preemption logic does not need to attempt preempting any pods when a pending pod cannot be scheduled because of its own affinity rules.

In order to keep backward compatibility, it would be better to keep the existing error (`ErrPodAffinityNotMatch`) and add three new ones which are returned in addition to  `ErrPodAffinityNotMatch`.

@kubernetes/sig-scheduling-feature-requests
