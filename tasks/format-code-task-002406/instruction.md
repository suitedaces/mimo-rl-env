## `network_false_nodes` drops the CRS of the input

I'm cleaning up a street network with `momepy.network_false_nodes` before feeding it into the rest of my workflow. My input GeoDataFrame has a proper CRS set (EPSG:27700 in my case), but the result coming out of `network_false_nodes` has no CRS attached anymore.

Minimal reproducer:

```python
import geopandas as gpd
import momepy

streets = gpd.read_file(...)        # projected, e.g. EPSG:27700
print(streets.crs)                  # EPSG:27700

cleaned = momepy.network_false_nodes(streets)
print(cleaned.crs)                  # None
```

Same thing happens when I pass a GeoSeries instead of a GeoDataFrame — the returned series has no CRS either.

This breaks downstream steps: I can't reproject the cleaned network, plotting it on top of a contextily basemap puts it in the wrong place, and any spatial join afterwards complains about mismatched / missing CRS. I have to manually re-assign `cleaned.crs = streets.crs` after every call, which feels like something the function should be preserving on its own.

Could `network_false_nodes` keep the CRS of the input on its return value (for both the GeoDataFrame and GeoSeries paths)?
