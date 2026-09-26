Handle minikube exit code 89
Minikube has well-defined exit codes, and Skaffold has special handling for turning minikube exit codes into actionable errors. This code needs to be updated as it's not handling minikube exit code 89:

```
invalid skaffold config: getting minikube env: running [/Users/bdealwis/installs/google-cloud-sdk/bin/minikube docker-env --shell none -p minikube --user=skaffold]
 - stdout: "false exit code 89\n"
 - stderr: ""
 - cause: exit status 89
```

Basically minikube is stopped.

- platform: macOS 12.3.1 on arm64
- `skaffold version`: v1.37.1 (installed via gcloud)
- `minikube version`:  v1.25.2 (installed via gcloud)
