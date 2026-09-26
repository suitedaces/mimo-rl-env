I'm looking for an ability to disable the metric extraction and ingestion into CloudWatch Metrics, while still logging them to CloudWatch Logs.

That ability is important for me as I want to be able to disable ingestion into CloudWatch Metrics on demand for cost saving purposes while still receiving the data in CloudWatch Logs enabling me to analytics with CloudWatch Insights, even though they aren't ingested into CloudWatch Metrics.

From reading through the EMF specification (https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html) I didn't notice any flag to indicate if metrics should be ingested into CloudWatch Metrics or not. 

Is there an option to choose whether such metrics should get ingested by CloudWatch Metrics or not? If not it'd be great to have such an option.

I'd expect this to be exposed as a config option, something like `Config.disable_metric_extraction` (with a matching `AWS_EMF_DISABLE_METRIC_EXTRACTION` environment variable).
