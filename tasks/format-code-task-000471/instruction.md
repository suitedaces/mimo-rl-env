Allow regex matching in S3KeySensorAsync
**Is your feature request related to a problem? Please describe.**
The wildcard matching uses `fnmatch.fnmatch` that uses unix wildcard pattern to filter bucket keys but it has a limitation. It cannot distinguish between `archived_uploads/dataset.csv` and `dataset.csv` when your wildcard pattern is `*.csv`. As S3 does not use directories, that wildcard pattern cannot filter "top level" bucket keys that do not have the delimeter `/`. Because of this, S3KeySensorAsync always goes in success state even if you have not uploaded anything new.

However, there is a workaround, which is to use some prefix in your bucket keys for new file uploads and to not upload at the top level. E.g. If you are uploading new files, upload them as `new/dataset.csv` and the wildcard pattern for this case will be `new/*.csv`.

**Describe the solution you'd like**
A flag variable `use_regex` when set to `True` should use regex pattern.

https://github.com/astronomer/astronomer-providers/blob/6b29b0428ca3a2f26c31dc6040f3a6f9b5d01d67/astronomer/providers/amazon/aws/hooks/s3.py#L151-L157

```python
                 elif use_regex:
                     keys = await self.get_file_metadata(client, bucket_name, key)
                     key_matches = [k for k in keys if re.match(pattern=key, string=k["Key"])]
                     if not key_matches:
                         return False
```

E.g. If you have bucket keys `archived_uploads/dataset1.csv`, `archived_uploads/dataset2.csv`, `archived_uploads/dataset3.csv` and `dataset4.csv`, this is the pattern you will need to only poke for keys that do not have the delimeter '/', in this case `dataset4.csv` does not have this delimeter: 

```python
S3KeySensorAsync(
    task_id='sense_datasets',
    bucket_name='default',
    # Negative Lookbehind regex pattern which tells regex to not match names that are being preceded by the delimeter "/".
    bucket_key=r'(?<!/)[a-zA-Z0-9_]+\.csv',
    use_regex=True,
)
```

**Describe alternatives you've considered**
Solved it via `check_fn`.

```python
def check_for_files_without_delimeter(files: list[dict[str, datetime.datetime | int | str | dict[str, str]]]) -> bool:
    if any((file_metadata for file_metadata in files if re.match(pattern=r'(?<!/)[\w_]+\.csv', string=file_metadata ['Key'], flags=re.IGNORECASE))):
        return True
    raise AirflowSkipException('No new files without the delimeter '/' are present.')
```
