If you have `None` in a geometry column, `dissolve` using shapely engine errors on AttributeError. I just encountered this in #2177.

```py
gpd.options.use_pygeos = False

nybb = gpd.read_file(gpd.datasets.get_path("nybb"))
nybb.loc[0, "geometry"] = None
nybb.dissolve("BoroCode")

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
/var/folders/kp/fxnnw89x5qbb9gryn507p03c0000gn/T/ipykernel_99971/1853337248.py in <module>
----> 1 nybb.dissolve("BoroCode")

~/Git/geopandas/geopandas/geodataframe.py in dissolve(self, by, aggfunc, as_index, level, sort, observed, dropna)
   1536             return merged_geom
   1537 
-> 1538         g = self.groupby(group_keys=False, **groupby_kwargs)[self.geometry.name].agg(
   1539             merge_geometries
   1540         )

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/pandas/core/groupby/generic.py in aggregate(self, func, engine, engine_kwargs, *args, **kwargs)
    263 
    264             try:
--> 265                 return self._python_agg_general(func, *args, **kwargs)
    266             except KeyError:
    267                 # TODO: KeyError is raised in _python_agg_general,

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/pandas/core/groupby/groupby.py in _python_agg_general(self, func, *args, **kwargs)
   1308             try:
   1309                 # if this function is invalid for this dtype, we will ignore it.
-> 1310                 result = self.grouper.agg_series(obj, f)
   1311             except TypeError:
   1312                 warnings.warn(

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/pandas/core/groupby/ops.py in agg_series(self, obj, func, preserve_dtype)
   1013             # In the datetime64tz case it would incorrectly cast to tz-naive
   1014             # TODO: can we get a performant workaround for EAs backed by ndarray?
-> 1015             result = self._aggregate_series_pure_python(obj, func)
   1016 
   1017             # we can preserve a little bit more aggressively with EA dtype

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/pandas/core/groupby/ops.py in _aggregate_series_pure_python(self, obj, func)
   1070             # Each step of this loop corresponds to
   1071             #  libreduction._BaseGrouper._apply_to_group
-> 1072             res = func(group)
   1073             res = libreduction.extract_result(res)
   1074 

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/pandas/core/groupby/groupby.py in <lambda>(x)
   1294     def _python_agg_general(self, func, *args, **kwargs):
   1295         func = com.is_builtin_func(func)
-> 1296         f = lambda x: func(x, *args, **kwargs)
   1297 
   1298         # iterate through "columns" ex exclusions to populate output dict

~/Git/geopandas/geopandas/geodataframe.py in merge_geometries(block)
   1533         # Process spatial component
   1534         def merge_geometries(block):
-> 1535             merged_geom = block.unary_union
   1536             return merged_geom
   1537 

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/pandas/core/generic.py in __getattr__(self, name)
   5485         ):
   5486             return self[name]
-> 5487         return object.__getattribute__(self, name)
   5488 
   5489     def __setattr__(self, name: str, value) -> None:

~/Git/geopandas/geopandas/base.py in unary_union(self)
    726         POLYGON ((0 1, 0 2, 2 2, 2 0, 1 0, 0 0, 0 1))
    727         """
--> 728         return self.geometry.values.unary_union()
    729 
    730     #

~/Git/geopandas/geopandas/array.py in unary_union(self)
    650 
    651     def unary_union(self):
--> 652         return vectorized.unary_union(self.data)
    653 
    654     #

~/Git/geopandas/geopandas/_vectorized.py in unary_union(data)
    892         return _pygeos_to_shapely(pygeos.union_all(data))
    893     else:
--> 894         return shapely.ops.unary_union(data)
    895 
    896 

/opt/miniconda3/envs/geo_dev/lib/python3.9/site-packages/shapely/ops.py in unary_union(self, geoms)
    157         subs = (c_void_p * L)()
    158         for i, g in enumerate(geoms):
--> 159             subs[i] = g._geom
    160         collection = lgeos.GEOSGeom_createCollection(6, subs, L)
    161         return geom_factory(lgeos.methods['unary_union'](collection))

AttributeError: 'NoneType' object has no attribute '_geom'
```
