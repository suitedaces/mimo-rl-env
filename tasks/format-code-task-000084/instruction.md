## `wrappers.vector.HumanRendering` doesn't actually render

I'm trying to use `gymnasium.wrappers.vector.HumanRendering` to show
several CartPole envs tiled in a single pygame window:

```python
import gymnasium as gym
from gymnasium.wrappers.vector import HumanRendering

envs = gym.make_vec("CartPole-v1", num_envs=3, render_mode="rgb_array")
envs = HumanRendering(envs)

obs, info = envs.reset()
for _ in range(100):
    envs.step(envs.action_space.sample())
envs.close()
```

The very first `reset()` call blows up and I never get a window. I
tried a few other configurations — different `num_envs`, passing a
custom `screen_size`, leaving it as `None` — and the failure mode
shifts around but the wrapper is never actually usable for me. I
can't get a single rendered frame out of it for any setup I tried.

Could someone take a look? Based on what I'm seeing it doesn't look
like the vector `HumanRendering` wrapper works at all in its current
state.
