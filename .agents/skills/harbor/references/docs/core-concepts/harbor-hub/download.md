> ## Documentation Index
> Fetch the complete documentation index at: https://docs.harborframework.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Download

> Download datasets, tasks, jobs, trials, and trajectories.

Harbor Hub is a shared storage layer for datasets, tasks, jobs, trials, and trajectories.

Users can upload data to the hub using the following commands.

```bash theme={"system"}
harbor run ... --upload
harbor upload "<job>"
harbor publish "<dataset>"
```

Downloading datasets and tasks from the hub is done using the `harbor download` command.

```bash theme={"system"}
harbor download "<dataset>"
harbor download "<task>"
```

Users may also download jobs, trials, and trajectories from the hub using the following commands.

```bash theme={"system"}
harbor job download "<job-id>"
harbor trial download "<trial-id>"
harbor trial download "<trial-id>" --trajectory
```

If you want to include retried trials in your download, include the `--include-retries` flag.
