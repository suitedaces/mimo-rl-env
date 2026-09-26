Make pandas.to_parquet handles partition columns better
#### Code Sample, a copy-pastable example if possible
Assuming `frame` is a pandas DataFrame which contains column `cal_dt`. If I want to write the DataFrame into a parquet partitioned by the column `cal_dt`, I have the following code without reading the doc carefully.
```python
frame.to_parquet('partitioned_parquet', partition_cols='cal_dt')
```

#### Problem description
The above code raises an issue of "KeyError: 'c'", which is not clear enough to users.

#### Expected Output
Of course, I know the right way is to pass a list of columns to `partition_cols` (see the code below).
```python
frame.to_parquet('partitioned_parquet', partition_cols=['cal_dt'])
```
However, as I mentioned that people will likely have the first example of code instead (expecting that passing a single column name would work) without reading the doc carefully. I think the method `to_parquet` should be enhanced to be either of the following.
1. Throws an exception with a clearer message saying that a list is required for `partition_cols` when a user passes a non-list object to it.
2. Support passing a single string to `partition_cols` in which it means to use that column as the partition column.
Either way, the implementation is simple but it does improve user experience.
