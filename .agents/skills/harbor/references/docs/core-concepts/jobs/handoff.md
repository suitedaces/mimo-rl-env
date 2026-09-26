> ## Documentation Index
> Fetch the complete documentation index at: https://docs.harborframework.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Handoff

> Resume a completed trial in your local agent CLI.

`harbor trial handoff` copies a completed trial's native session to your local
agent CLI and resumes it in the current directory. Use it to continue the
conversation or ask the agent about its work.

```bash theme={"system"}
# Local trial directory
harbor trial handoff "jobs/<job>/<trial>"

# Harbor Hub trial ID
harbor trial handoff 594025f3-7d65-4655-8576-4bee95002eae
```

<Frame caption="Trial handoff to Claude Code">
  <video controls className="w-full aspect-video rounded-xl" src="https://mintcdn.com/harborframework/l9c_ohETpnOqpDv2/videos/handoff-demo.mp4?fit=max&auto=format&n=l9c_ohETpnOqpDv2&q=85&s=d07645a30c2c0555004caa485aea86ad" data-path="videos/handoff-demo.mp4">
    Your browser does not support video playback.
  </video>
</Frame>

For a Hub trial ID, Harbor downloads the trial first. For `claude-code`, handoff
copies the session to the local Claude Code store and runs
`claude --resume <session-id>`.

## Requirements

* The agent supports `capabilities.handoff`. Currently, only `claude-code` does.
* The agent CLI is installed locally. For `claude-code`, `claude` must be on `PATH`.
* The trial contains one session. Multi-session trials are not supported.

## What is restored

Handoff restores the native session history, not files from the trial sandbox.
See [Loading trajectories](/core-concepts/jobs/loading-trajectories) to seed a
new Harbor run instead.
