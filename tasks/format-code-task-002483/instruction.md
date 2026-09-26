Can't set nodata value to `inf` / `-inf`
## Expected behavior and actual behavior.

`inf`, `-inf` are valid nodata values in GDAL. 


## Steps to reproduce the problem.

```python
import rasterio
from rasterio.io import MemoryFile

with MemoryFile() as mem:
    with mem.open(driver="GTiff", width=1, height=1, count=1, dtype='float32', nodata=float('inf')) as src:
         print(src.nodata)

---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-21-e1f368f0f629> in <module>
      1 with MemoryFile() as mem:
----> 2     with mem.open(driver="GTiff", width=1, height=1, count=1, dtype='float32', nodata=float('inf')) as src:
      3         print(src.nodata)
      4 
      5 

~/Dev/venv/python38/lib/python3.8/site-packages/rasterio/env.py in wrapper(*args, **kwds)
    382     def wrapper(*args, **kwds):
    383         if local._env:
--> 384             return f(*args, **kwds)
    385         else:
    386             with Env.from_defaults():

~/Dev/venv/python38/lib/python3.8/site-packages/rasterio/io.py in open(self, driver, width, height, count, crs, transform, dtype, nodata, sharing, **kwargs)
    132         else:
    133             writer = get_writer_for_driver(driver)
--> 134             return writer(mempath, 'w+', driver=driver, width=width,
    135                           height=height, count=count, crs=crs,
    136                           transform=transform, dtype=dtype,

rasterio/_io.pyx in rasterio._io.DatasetWriterBase.__init__()

ValueError: Given nodata value, inf, is beyond the valid range of its data type, float32.
```

I need to dig deeper but to me it seems the error comes from https://github.com/mapbox/rasterio/blob/db03b66e81b489d3f5f01c9edfb6fc720250a2c1/rasterio/_io.pyx#L309-L311

Just noting when editing nodata value from an opened file I don't get error but the nodata is then set to None 

```python
import rasterio
with rasterio.open("test.tif", "w", driver="GTiff", width=1, height=1, count=1, dtype='float32') as src:
    print(src.nodata)
>> None

with rasterio.open("test.tif", "r+") as src:
    src._set_nodatavals((float("-inf"),))
    print(src.nodata)
>> -inf

with rasterio.open("test.tif", "r") as src:
    print(src.nodata)
>> None
```

## Operating system

Mac OS X M1 

## Rasterio version and provenance

rasterio 1.2.6 built from sources with GDAL 3.2.2
