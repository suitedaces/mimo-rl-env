[Bug]: opentracing configuration in configmap attempts to be utilized even when set to disabled
### Version

3.7.1

### What Kubernetes platforms are you running on?

EKS Amazon

### Steps to reproduce

Apply the following items in the nginx-ingress configmap
```
  opentracing: "False"
  opentracing-tracer: /usr/local/lib/libzipkin_opentracing_plugin.so
  opentracing-tracer-config: '{"collector_host":null,"sample_rate":1,"service_name":"nginx-ingress"}'
```

It is expected that the first setting `opentracing: "False"` should completely disable the feature, but instead the subsequent two opentracing fields are consumed and applied to the live nginx.conf. Since the tracer-config is invalid, it results in crashloop due to nginx.conf not being valid.

I would expect that disabling opentracing prevents the tracer-config from being used in nginx.conf. Instead I need to remove all of these items from the configmap rather than just switching the disable setting.
