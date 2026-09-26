Canary 2.7.0 Push Mode Always Uses HTTP
<!-- Please keep the structure below, or your issue may be closed. -->

**Describe the bug**
Canary push mode uses HTTP even if `-tls=true` is set.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure Loki with a HTTPS frontend (we use AWS ALB).
2. Start canary with the following configuration:

`[
  "-addr=loki-internal.alb:443",
  "-interval=10s",
  "-labelname=canary-id",
  "-labelvalue=canary-1234",
  "-push",
  "-tls=true",
  "-streamname=source",
  "-streamvalue=stdout",
  "-user=<LOKI_USER>",
  "-pass=<LOKI_PASSWORD>"
]`

**Expected behavior**
When `-tls=true` is set I'd expect Canary to use HTTPS when pushing.

**Environment:**
 - Infrastructure: AWS ECS
 - Deployment tool: Terraform

**Screenshots, Promtail config, or terminal output**
With above configuration, we get the following logs from ALB:

`https 2022-11-15T00:34:21.063192Z app/loki-internal-alb/ghasjhya <IP>:56178 - -1 -1 -1 400 - 256 370 "POST http://loki-internal.alb:443/loki/api/v1/push HTTP/1.1" "canary-push/2.7.0" - - - "-" "-" "-" - 2022-11-15T00:34:21.062000Z "-" "-" "-" "-" "-" "-" "-"`
