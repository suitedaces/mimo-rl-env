SplunkHecExporter doesn't ingest Resources
**Describe the bug**
ResourceLog's Resource labels are not ingested but only Attributes. 
I am ingesting this log
```
2021-03-20T00:05:40.172Z        INFO    loggingexporter/logging_exporter.go:471 LogsExporter    {"#logs": 1}
2021-03-20T00:05:40.173Z        DEBUG   loggingexporter/logging_exporter.go:498 ResourceLog #0
Resource labels:
     -> k8spoduid: STRING(eda0a956-99ec-49cb-a954-d733e2f881dd)
     -> k8s.pod.annotations.splunk.com/index: STRING(test)
     -> k8s.pod.name: STRING(loggen-zjklf)
     -> k8s.namespace.name: STRING(default)
     -> k8s.pod.startTime: STRING(2021-03-20 00:03:32 +0000 UTC)
     -> k8s.pod.uid: STRING(eda0a956-99ec-49cb-a954-d733e2f881dd)
     -> k8s.node.name: STRING(ip-192-168-82-91.us-west-1.compute.internal)
     -> k8s.pod.labels.hello: STRING(loggen)
     -> k8s.pod.labels.app: STRING(loggen)
InstrumentationLibraryLogs #0
InstrumentationLibrary  
LogRecord #0
Timestamp: 1616198740006040006
Severity: Undefined
ShortName: 
Body: {
     -> log: STRING(num: 127 | loggen-zjklf | 2021-03-20T00:05:40.005870 | rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
)
}
Attributes:
     -> k8s.pod.uid: STRING(eda0a956-99ec-49cb-a954-d733e2f881dd)
     -> run_id: STRING(0)
     -> stream: STRING(stdout)
     -> k8s.container.name: STRING(loggen)
     -> k8s.namespace.name: STRING(default)
     -> k8s.pod.name: STRING(loggen-zjklf)
```
**Steps to reproduce**
read container logs using `fileread` and enrich it with `k8s_tagger` then export using SplunkHecExporter

**What did you expect to see?**
See log data with both attributes and resource labels.

**What did you see instead?**
![image](https://user-images.githubusercontent.com/12387289/111940051-0c840d00-8a8b-11eb-8ed5-3509c74a4f4e.png)
I do not see resource labels.

**What version did you use?**
0.22.0

**What config did you use?**
```
exporters:
  logging:
    loglevel: debug
    sampling_initial: 5
    sampling_thereafter: 2000
  splunk_hec:
    disable_compression: true
    endpoint: https://0.0.0.0:8088/services/collector
    index: k8s_log
    insecure_skip_verify: true
    max_connections: 2000
    source: otel
    sourcetype: otel
    timeout: 10s
    token: XXXXXX
extensions:
  health_check: {}
processors:
  batch: {}
  k8s_tagger:
    auth_type: kubeConfig
    extract:
      annotations:
      - key: splunk.com/index
      labels:
      - key: hello
      - key: app
      metadata:
      - podName
      - podUID
      - deployment
      - cluster
      - namespace
      - node
      - startTime
    filter:
      node_from_env_var: KUBE_NODE_NAME
    passthrough: false
    pod_association:
    - from: resource_attribute
      name: k8spoduid
  memory_limiter:
    ballast_size_mib: 409
    check_interval: 5s
    limit_mib: 819
    spike_limit_mib: 256
receivers:
  filelog:
    exclude:
    - /var/log/pods/default_otel-opentelemetry-collector-agent-*_*/opentelemetry-collector/*.log
    include:
    - /var/log/pods/*/*/*.log
    include_file_name: false
    include_file_path: true
    operators:
    - id: parser-docker
      output: extract_metadata_from_filepath
      timestamp:
        layout: '%Y-%m-%dT%H:%M:%S.%LZ'
        parse_from: time
      type: json_parser
    - id: extract_metadata_from_filepath
      parse_from: $$attributes.file_path
      regex: ^\/var\/log\/pods\/(?P<namespace>[^_]+)_(?P<pod_name>[^_]+)_(?P<uid>[^\/]+)\/(?P<container_name>[^\._]+)\/(?P<run_id>\d+)\.log$
      type: regex_parser
    - attributes:
        k8s.container.name: EXPR($.container_name)
        k8s.namespace.name: EXPR($.namespace)
        k8s.pod.name: EXPR($.pod_name)
        k8s.pod.uid: EXPR($.uid)
        run_id: EXPR($.run_id)
        stream: EXPR($.stream)
      resource:
        k8spoduid: EXPR($.uid)
      type: metadata
    - id: clean-up-log-record
      ops:
      - remove: logtag
      - remove: stream
      - remove: container_name
      - remove: namespace
      - remove: pod_name
      - remove: run_id
      - remove: uid
      type: restructure
    start_at: beginning
service:
  extensions:
  - health_check
  pipelines:
    logs:
      exporters:
      - logging
      - splunk_hec
      processors:
      - batch
      - k8s_tagger
      receivers:
      - filelog

```
**Environment**
docker container 
go: 1.15
**Additional context**
