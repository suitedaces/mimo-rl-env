DOC/DEPR: sep vs pat in series.str.partition
All the way back to the v0.16 docs, `Series.str.partition` (https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.partition.html) has the signature ```Series.str.partition(pat=' ', expand=True)```, but the docs only talk about `sep` instead of `pat`.
![3](https://user-images.githubusercontent.com/33685575/45404837-d4511780-b660-11e8-865f-e64bd2f47852.png)

I think the kwarg should be renamed to `sep`, which makes more sense for partitioning something than `pat`, which sounds like it's about a regex pattern.

Same thing applies to `rpartition`.
