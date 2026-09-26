BUG: NaN now None when calling df.apply? (0.10.2 -> 0.11)
- [X] I have checked that this issue has not already been reported.
- [X] I have confirmed this bug exists on the latest version of geopandas.

---
y information for us to reproduce your bug.

#### Code Sample, a copy-pastable example

```python
def test_geopanda(request):
    geojson_path = path.join(request.fspath.dirname, "test_data/test.geojson")
    x = gpd.read_file(geojson_path)
    x["test_calc"] = x.apply(
        lambda x: float('NaN'),
        axis=1,
    )
    assert math.isnan(x["test_calc"][0])
```

#### Problem description

Previously when our lambda inside apply returned NaN, the result of `apply` was NaN for all rows. When upgrading to 0.11, it now returns NoneType instead. I couldn't see this documented as a known breaking change anywhere?

#### Expected Output

Test passes in 0.10.2, fails in 0.11

#### Output of ``geopandas.show_versions()``

<details>

SYSTEM INFO
-----------
python     : 3.9.13 | packaged by conda-forge | (main, May 27 2022, 17:01:00)  [Clang 13.0.1 ]
executable : /Users/jcrowley/miniconda3/envs/dataprocessing_env/bin/python3
machine    : macOS-12.3.1-arm64-arm-64bit

GEOS, GDAL, PROJ INFO
---------------------
GEOS       : 3.10.3
GEOS lib   : /Users/jcrowley/miniconda3/envs/dataprocessing_env/lib/libgeos_c.dylib
GDAL       : 3.5.0
GDAL data dir: /Users/jcrowley/miniconda3/envs/dataprocessing_env/share/gdal
PROJ       : 9.0.1
PROJ data dir: /Users/jcrowley/miniconda3/envs/dataprocessing_env/share/proj

PYTHON DEPENDENCIES
-------------------
geopandas  : 0.11.0
pandas     : 1.4.3
fiona      : 1.8.21
numpy      : 1.23.0
shapely    : 1.8.2
rtree      : 1.0.0
pyproj     : 3.3.1
matplotlib : 3.5.2
mapclassify: 2.4.3
geopy      : None
psycopg2   : None
geoalchemy2: None
pyarrow    : None
pygeos     : None

</details>
