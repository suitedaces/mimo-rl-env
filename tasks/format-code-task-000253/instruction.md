# Add per-node execution timeout support to taskflow

Operators want individual task nodes to be guarded by an execution timeout. When a node runs
longer than its configured limit, the system should be able to react automatically according to a
per-node strategy. This change is about the *building blocks* of that feature — the configuration
parsing, the timeout-handling strategies, and an up-front validation guard. (The Celery/Redis
machinery that periodically scans for timed-out nodes is out of scope here.)

A node's timeout is described on the node itself, inside a `timeout_config` object, e.g.:

```json
"timeout_config": {"enable": true, "seconds": 30, "action": "forced_fail"}
```

Please implement the following observable behavior.

## 1. Parsing timeout configuration from a pipeline tree

Provide a function `parse_node_timeout_configs`, importable from `gcloud.taskflow3.utils`, that
takes a fully expanded pipeline tree (a dict whose `"activities"` maps node ids to node dicts) and
returns the list of timeout configurations declared in it.

- Each returned item is a dict with exactly the keys `node_id`, `action`, and `timeout`, where
  `timeout` is the configured number of seconds and `action` is the configured action string.
- Only `ServiceActivity` nodes that have `timeout_config` with a truthy `enable` produce a config.
  A node without `timeout_config`, or with `enable` falsy/absent, produces nothing.
- `SubProcess` nodes never produce a config themselves, but their nested pipeline (under the node's
  `"pipeline"` key) must be traversed recursively so that timeout configs declared at any depth are
  collected.
- The configured `seconds` must be a positive integer. If `seconds` is missing, not an integer, or
  not greater than zero, that node is skipped (no config is produced for it) but parsing of the rest
  of the tree continues normally.
- The order of the returned configs is not significant.

## 2. Timeout-handling strategies

Provide a registry `node_timeout_handler`, importable from
`gcloud.taskflow3.domains.node_timeout_strategy`, that maps an action string to a strategy object.
Each strategy object exposes a method `deal_with_timeout_node(task, node_id)` that enforces the
timeout against the given task by driving the task's node-action API (`task.nodes_action(action,
node_id, operator)`), acting as a fixed system operator. `nodes_action` returns a dict whose
`"result"` key indicates success.

Two actions must be supported:

- `"forced_fail"`: force-fail the node (a single `forced_fail` node action) and return that action's
  result.
- `"forced_fail_and_skip"`: force-fail the node first; **only if** the force-fail result indicates
  success, then skip the node (a `skip` node action) and return the skip result. If the force-fail
  did not succeed, return the force-fail result and do not attempt to skip.

## 3. Conflict validation when converting web data to a pipeline

Enabling a node's timeout is incompatible with the node ignoring errors or auto-retrying — letting a
node both retry/ignore-failure and be force-failed on timeout is contradictory. When web pipeline
data is converted into an executable pipeline, a `ServiceActivity` that has `timeout_config` enabled
together with either `error_ignorable` enabled or `auto_retry` enabled must be rejected by raising
`pipeline.exceptions.InvalidOperationException`. A node that enables its timeout without those
conflicting options must continue to convert successfully.
