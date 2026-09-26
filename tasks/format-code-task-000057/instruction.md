## Custom auto multi-line samples 通过环境变量配置时不生效

我在 Kubernetes 里跑 datadog-agent，所有配置都走环境变量（不挂 datadog.yaml）。最近想用 auto multi-line detection 的 custom samples 功能聚合一些应用日志。

按照文档把配置写在 datadog.yaml 里测试是没问题的，比如：

```yaml
logs_config:
  auto_multi_line_detection_custom_samples:
    - sample: "2024-01-01 00:00:00"
      label: start_group
    - regex: "^\\[ERROR\\]"
      label: start_group
```

agent 重启后能正确识别我的多行日志。

但是搬到容器部署、改成环境变量后就不工作了：

```
DD_LOGS_CONFIG_AUTO_MULTI_LINE_DETECTION_CUSTOM_SAMPLES='[{"sample":"2024-01-01 00:00:00","label":"start_group"},{"regex":"^\\[ERROR\\]","label":"start_group"}]'
```

agent 起来后这些 custom samples 完全没生效，日志还是按默认逻辑拆，并且 agent 日志里能看到一行 unmarshal custom samples 失败的错误。

其它列表型的配置（比如 tags、`DD_CONTAINER_EXCLUDE` 那一类）以 JSON 字符串形式传 env var 都是正常工作的，所以希望这个配置项也能支持同样的用法 —— 容器化部署里没法只靠 YAML。
