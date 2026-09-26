Scrape-config jobs with same name occur crashloop in prometheus
<!--

Feel free to ask questions in #prometheus-operator on Kubernetes Slack!

-->

**What happened?**
Prometheus created scrape config jobs with same name after creation of a Servicemonitor and Podmonitor with the same name in the same namespace. After trying to reload /etc/prometheus/config_out/prometheus.env.yaml Prometheus crashed and keeps in status CrashLoopBackOff. 

**Did you expect to see some different?**
Prometheus should stop reloading in case the /etc/prometheus/config_out/prometheus.env.yaml file is not valid and should not crash. Additionally Prometheus should prevent updating the configuration file that it becomes invalid.

**How to reproduce it (as minimally and precisely as possible)**:
- create Prometheus with kube-prometheus-stack helm chart 
- create a ServiceMonitor and a PodMonitor with the same name in the same namespace 

**Environment**


* Prometheus Operator version:
0.45.0 (deployed by kube-prometheus-stack helm chart)

* Kubernetes version information:
kubernetes 1.17.* 

* Kubernetes cluster kind:
Amazon EKS service

* Manifests:

* Prometheus Operator Logs:

* Prometheus Logs:
level=error ts=2021-02-18T14:20:44.401Z caller=main.go:293 msg="Error loading config (--config.file=/etc/prometheus/config_out/prometheus.env.yaml)" err="parsing YAML file /etc/prometheus/config_out/prometheus.env.yaml: found multiple scrape configs with job name \"default/testmonitor/0\""

**Anything else we need to know?**:
Additional scrape configs set:
```
- job_name: 'kubernetes-service-endpoints'
  kubernetes_sd_configs:
    - role: endpoints
  relabel_configs:
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
      action: replace
      target_label: __scheme__
      regex: (https?)
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
      action: replace
      target_label: __address__
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_service_name]
      action: replace
      target_label: kubernetes_name
    - source_labels: [__meta_kubernetes_service_name]
      action: drop
      regex: 'node-exporter'
- job_name: 'kubernetes-pods'
  kubernetes_sd_configs:
    - role: pod
  relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      target_label: __address__
    - action: labelmap
      regex: __meta_kubernetes_pod_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_pod_name]
      action: replace
      target_label: kubernetes_pod_name
```
