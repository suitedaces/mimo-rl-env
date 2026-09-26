BigQueryCreateDataTransferOperator will log AWS credentials when transferring from S3
### Apache Airflow Provider(s)

google

### Versions of Apache Airflow Providers

[apache-airflow-providers-google 8.6.0](https://airflow.apache.org/docs/apache-airflow-providers-google/8.6.0/)



### Apache Airflow version

2.5.0

### Operating System

Debian GNU/Linux 11 (bullseye)

### Deployment

Official Apache Airflow Helm Chart

### Deployment details

_No response_

### What happened

When creating a transfer config that will move data from AWS S3, an access_key_id and secret_access_key are provided (see: https://cloud.google.com/bigquery/docs/s3-transfer).

These parameters are logged and exposed as XCom return_value.

### What you think should happen instead

At least the secret_access_key should be hidden or removed from the XCom return value

### How to reproduce

```
PROJECT_ID=123
TRANSFER_CONFIG={
                "destination_dataset_id": destination_dataset,
                "display_name": display_name,
                "data_source_id": "amazon_s3",
                "schedule_options": {"disable_auto_scheduling": True},
                "params": {
                    "destination_table_name_template": destination_table,
                    "file_format": "PARQUET",
                    "data_path": data_path,
                    "access_key_id": access_key_id,
                    "secret_access_key": secret_access_key
                }
            },

gcp_bigquery_create_transfer = BigQueryCreateDataTransferOperator(
    transfer_config=TRANSFER_CONFIG,
    project_id=PROJECT_ID,
    task_id="gcp_bigquery_create_transfer",
)
```

### Anything else

_No response_

### Are you willing to submit PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
