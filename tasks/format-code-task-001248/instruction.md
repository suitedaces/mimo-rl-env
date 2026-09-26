BUG: preserve spatial_partitions in GeoDataFrame.set_crs
Currently, using `set_crs` doesn't preserve the spatial partitions (similar as `copy`, see https://github.com/geopandas/dask-geopandas/pull/56):

```python
import geopandas
import dask_geopandas

gdf = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
# remove the crs for purpose of the reproducible example
gdf.crs = None

# create partitioned dataframe + calculate spatial partitions
ddf = dask_geopandas.from_geopandas(gdf, npartitions=4)
ddf.calculate_spatial_partitions()

>>> ddf.spatial_partitions
0    POLYGON ((-68.149 -55.612, -68.640 -55.580, -6...
1    POLYGON ((18.465 -29.045, 16.345 -28.577, -77....
2    POLYGON ((166.740 -22.400, -8.899 36.869, -9.5...
3    POLYGON ((-180.000 -90.000, -180.000 -84.713, ...
dtype: geometry
>>> ddf = ddf.set_crs("EPSG:4326")
>>> ddf.spatial_partitions is None
True
```
