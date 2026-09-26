## Problem Statement

我搭了个 pipeline，source 用的是 serving，中间有个 udf 用了 groupBy 做 reduce 聚合。kubectl apply 是过了的，Pod 也都起来了，但跑起来怎么都不对劲，往 serving 端点打请求拿不到回调结果，看 vertex 日志也没啥明显报错。我一开始以为是自己 groupBy 的 window 配错了，换了几种 window 都一样。这种组合（serving source + reduce）到底是支不支持？如果不支持，至少 apply 的时候能让我知道一下啊，现在这样我根本不知道是配错了还是本来就不行。

## Expected outcomes

- Pipeline validation:
  - A pipeline that combines a Serving source with any reduce UDF vertex must be rejected during validation, so applying that manifest fails before the pipeline is admitted.
  - The validation error should clearly identify both the Serving source vertex and the reduce vertex, and should state that reduce is not supported with a Serving source.
  - Pipelines that have a Serving source but no reduce vertex, and pipelines that have reduce vertices but no Serving source, should continue to validate when they are otherwise valid.

- Serving source pod layout and configuration:
  - The generated pod spec for a Serving source vertex should not include a separate serving-specific sidecar container; the serving-related runtime configuration should be available on the main Numaflow container.
  - The main container for a Serving source vertex should receive the serving pipeline metadata needed for callback handling, including the minimal pipeline specification, serving listen port, and pod IP source.
  - Callback enablement should be explicit for pipelines that contain at least one Serving source: every vertex main container in such a pipeline should have callback enabled.
  - Callback URL environment configuration should not be injected into vertex main containers.
  - Pipelines without a Serving source should not receive Serving callback environment configuration.

## Implementation notes

- The validation location, data structures, and traversal strategy are up to the implementer, as long as the externally observable validation behavior is correct.
- The pod-spec construction may be reorganized as needed, but tests should be satisfied through the observable generated Kubernetes pod spec rather than by relying on a particular private helper or internal call path.
- Preserve existing valid pipeline behavior except where the Serving-source-plus-reduce combination is intentionally rejected.
