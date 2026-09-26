## Problem Statement

I'm seeing weird samples when I train DQN/DDPG with batched environments and replay: n-step sequences and episodic replay entries sometimes contain transitions from different parallel envs stitched together. It also looks like when one batch item hits done/reset, the replay state for the other still-running envs gets disturbed. This shows up with interleaved env steps where sampled trajectories have state/action markers from multiple envs.

## Expected outcomes

- Sampled n-step replay sequences never combine transitions from different parallel environment sources, including when environment steps are interleaved.
- Calling `stop_current_episode(env_id=...)` ends only the replay trajectory for that environment and does not flush, clear, or mix trajectories from other environments.
- Stored and sampled episodic replay entries never combine transitions from different parallel environment sources, including when episodes are completed or interrupted in a different order than their steps were observed.
- In DQN/DDPG batch training with replay, each batch position is handled as a distinct replay environment identity, and a done/reset flag for one batch position does not disturb the replay trajectory for other batch positions.
- `ReplayBuffer.append` accepts additional keyword fields and preserves them in stored experiences so they can be observed after sampling.

## Implementation notes

The exact internal data structures, storage layout, and validation locations are up to the implementation. Preserve existing single-environment behavior by treating omitted environment identity as the default environment.

## Required public API surface (mechanical binding)

The following names / signatures MUST be implemented exactly as listed; downstream test harness mechanically binds these:

- `ReplayBuffer.append(..., env_id=..., **kwargs)` and equivalent concrete replay-buffer append methods - tests must pass a named public environment identity to create multiple replay streams through the buffer API, while still verifying arbitrary extra keyword fields are stored.
