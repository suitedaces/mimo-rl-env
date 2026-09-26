Default "skew angle" for CF grid mapping "oblique mercator" seems wrong
Hi!

When using `pyproj.CRS.from_cf` on attributes defining an oblique mercator grid mapping, it seems that the Pyproj projection if rotated 90° from the expected output.  Specifically, I think this line should assign 90, not 0 : 
https://github.com/pyproj4/pyproj/blob/b7b8384804995c1729b5373f7923238821640b68/pyproj/crs/_cf1x8.py#L237


I am plotting data from a climate model that runs on the oblique mercator projection. In this first plot, the cartopy CRS was obtained with : `cartopy.crs.Projection(pyproj.CRS.from_cf(oblique_mercator))`:

<img width="374" height="182" alt="Image" src="https://github.com/user-attachments/assets/19fc369c-3b77-4372-ac4c-451074449fe0" />

In this second plot, I instead used cartopy's implementation of the same,  `cartopy.crs.ObliqueMercator` :

<img width="374" height="182" alt="Image" src="https://github.com/user-attachments/assets/c5d5e071-94cf-4094-9fe9-fb5083502414" />

We can clearly see that the second figure is what we expected.

The grid mapping variable has the following attributes:
```python3
{'grid_mapping_name': 'oblique_mercator',
 'azimuth_of_central_line': 90.0,
 'latitude_of_projection_origin': 46.0,
 'longitude_of_projection_origin': 263.0,
 'scale_factor_at_projection_origin': 1.0,
 'false_easting': 0.0,
 'false_northing': 0.0}
```

The [CF conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#_oblique_mercator) do not define the "Angle from Rectified to Skew Grid". In cartopy, it is not specified, so the default is used. In pyproj, it is specified as 0°. From, [this page](http://geotiff.maptools.org/proj_list/hotine_oblique_mercator.html), I gather that the default value should be 90°. And indeed, we are seeing a 90° degree rotation when using pyproj's projection object.

Thus why I think the value in pyproj is wrong.
