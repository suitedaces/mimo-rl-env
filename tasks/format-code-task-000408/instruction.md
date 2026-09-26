GCSToBigQueryOperator fails when schema_object is specified without schema_fields
### Apache Airflow Provider(s)

google

### Versions of Apache Airflow Providers

apache-airflow 2.5.0
apache-airflow-providers-apache-beam 4.1.0
apache-airflow-providers-cncf-kubernetes 5.0.0
apache-airflow-providers-google 8.6.0
apache-airflow-providers-grpc 3.1.0

### Apache Airflow version

2.5.0

### Operating System

Debian 11

### Deployment

Official Apache Airflow Helm Chart

### Deployment details

KubernetesExecutor

### What happened

GCSToBigQueryOperator allows multiple ways to specify schema of the BigQuery table:

1. Setting autodetect == True
1. Setting schema_fields directly with autodetect == False
1. Setting a schema_object and optionally a schema_object_bucket with autodetect == False

This third method seems to be broken in the latest provider version (8.6.0) and will always result in this error:

```
[2022-12-16, 21:06:18 UTC] {taskinstance.py:1772} ERROR - Task failed with exception
Traceback (most recent call last):
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/providers/google/cloud/transfers/gcs_to_bigquery.py", line 395, in execute
    self.configuration = self._check_schema_fields(self.configuration)
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/providers/google/cloud/transfers/gcs_to_bigquery.py", line 524, in _check_schema_fields
    raise RuntimeError(
RuntimeError: Table schema was not found. Set autodetect=True to automatically set schema fields from source objects or pass schema_fields explicitly
```

The reason for this is because [this block](https://github.com/apache/airflow/blob/25bdbc8e6768712bad6043618242eec9c6632618/airflow/providers/google/cloud/transfers/gcs_to_bigquery.py#L318-L320) where `if self.schema_object and self.source_format != "DATASTORE_BACKUP":`. fails to set self.schema_fields. It only sets the local variable, schema_fields. When self._check_schema_fields is subsequently called [here](https://github.com/apache/airflow/blob/25bdbc8e6768712bad6043618242eec9c6632618/airflow/providers/google/cloud/transfers/gcs_to_bigquery.py#L395), we enter the [first block](https://github.com/apache/airflow/blob/25bdbc8e6768712bad6043618242eec9c6632618/airflow/providers/google/cloud/transfers/gcs_to_bigquery.py#L523-L528) because autodetect is false and schema_fields is not set.

### What you think should happen instead

No error should be raised if autodetect is set to False and a valid schema_object is provided

### How to reproduce

1. Create a simple BigQuery table with a single column col1:

```sql
CREATE TABLE `my-project.my_dataset.test_gcs_to_bigquery` (col1 INT);
```

2. Upload a json blob for this object to a bucket (e.g., data/schemas/table.json)
3. Upload a simple CSV for the source file to load to a bucket (e.g., data/source/file.csv)
4. Run the following command:

```py
    gcs_to_biquery = GCSToBigQueryOperator(
        task_id="gcs_to_bigquery",
        destination_project_dataset_table="my-project.my_dataset.test_gcs_to_bigquery",
        bucket="my_bucket_name",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        source_objects=["data/source/file.csv"],
        source_format="CSV",
        autodetect=False,
        schema_object="data/schemas/table.json",
    )
```

### Anything else

_No response_

### Are you willing to submit PR?

- [X] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
