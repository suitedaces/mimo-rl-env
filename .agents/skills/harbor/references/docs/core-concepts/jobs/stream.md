> ## Documentation Index
> Fetch the complete documentation index at: https://docs.harborframework.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Stream

> Follow agent actions and explore sandbox files while a job runs.

See what the agent is doing and inspect its work while a job runs:

1. **Stream agent logs.** Follow agent actions, commands, and results in the
   **Trajectory** tab as new steps arrive.
2. **Watch the agent's directory.** Open the **Stream** tab to browse sandbox
   files and generated artifacts in real time. It connects automatically after sandbox is ready.

<Frame>
  <video controls preload="metadata" className="w-full rounded-xl" src="https://mintcdn.com/harborframework/W_p3l7T0HwYv0Zsi/videos/stream-demo.mp4?fit=max&auto=format&n=W_p3l7T0HwYv0Zsi&q=85&s=27dce4e804f7d1850e39343583434a6d" aria-label="Sandbox files in the Stream tab alongside live agent steps in the Trajectory tab" data-path="videos/stream-demo.mp4">
    Your browser does not support embedded video.
  </video>
</Frame>

Add `--stream` to your run. Currently supports Claude Code and Codex on Daytona, Modal, Tensorlake, or local Docker:

```bash theme={"system"}
harbor run -t terminal-bench/build-cython-ext \
  -a claude-code -m anthropic/claude-sonnet-5 -e docker --stream
```

In another terminal:

```bash theme={"system"}
harbor view jobs
```

Run the browser and viewer on the same machine.
For Daytona, make credentials available to both Harbor **and the viewer**.

Add `--no-delete` to keep the sandbox available after the run. **This is also useful for debugging.** Don't forget to delete later.
