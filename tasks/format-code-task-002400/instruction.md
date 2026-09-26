Export as WKT1_ESRI or WKT1_GDAL silently returns None for custom CRS
<!-- Please search existing issues to avoid creating duplicates. -->


#### Code Sample, a copy-pastable example if possible

```python
import pyproj

crs_wkt = 'PROJCRS["unknown",BASEGEOGCRS["unknown",DATUM["unknown",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1,ID["EPSG",9001]]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8901]]],CONVERSION["unknown",METHOD["Equidistant Cylindrical",ID["EPSG",1028]],PARAMETER["Latitude of 1st standard parallel",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8823]],PARAMETER["Longitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8802]],PARAMETER["False easting",0,LENGTHUNIT["unknown",111319.490793274],ID["EPSG",8806]],PARAMETER["False northing",0,LENGTHUNIT["unknown",111319.490793274],ID["EPSG",8807]]],CS[Cartesian,3],AXIS["(E)",east,ORDER[1],LENGTHUNIT["unknown",111319.490793274]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["unknown",111319.490793274]],AXIS["ellipsoidal height (h)",up,ORDER[3],LENGTHUNIT["metre",1,ID["EPSG",9001]]]]'

crs = pyproj.CRS.from_user_input(crs_wkt)
crs.to_wkt(version="WKT1_ESRI")
```
#### Problem description

Export of the custom CRS used above to WKT using `version="WKT1_ESRI"` returns None. My assumption is that the CRS cannot be expressed as WKT1_ESRI but pyproj does not raise or warn about it but happily returns `None` instead. The CRS is coming from https://github.com/geopandas/geopandas/issues/2387.

#### Expected Output

I would expect this to raise or give me some sort of indication that the export did not happen.

#### Environment Information
```
pyproj info:
    pyproj: 3.2.1
      PROJ: 8.1.1
  data dir: /Users/martin/mambaforge/envs/geo_dev/share/proj
user_data_dir: /Users/martin/Library/Application Support/proj

System:
    python: 3.9.7 | packaged by conda-forge | (default, Sep 29 2021, 19:24:02)  [Clang 11.1.0 ]
executable: /Users/martin/mambaforge/envs/geo_dev/bin/python
   machine: macOS-12.3-arm64-arm-64bit

Python deps:
   certifi: 2021.10.08
       pip: 21.3.1
setuptools: 58.5.3
    Cython: 0.29.24
```

#### Installation method
 - conda-forge

#### Conda environment information (if you installed with conda):

<br/>
Environment (<code>conda list</code>):
<details>

```
$ conda list proj
# packages in environment at /Users/martin/mambaforge/envs/geo_dev:
#
# Name                    Version                   Build  Channel
proj                      8.1.1                h2d984c1_2    conda-forge
pyproj                    3.2.1            py39had8e633_2    conda-forge
```
</details>

<br/>
Details about  <code>conda</code> and system ( <code>conda info</code> ):
<details>

```
$ conda info

     active environment : geo_dev
    active env location : /Users/martin/mambaforge/envs/geo_dev
            shell level : 2
       user config file : /Users/martin/.condarc
 populated config files : /Users/martin/mambaforge/.condarc
                          /Users/martin/.condarc
          conda version : 4.10.3
    conda-build version : not installed
         python version : 3.9.7.final.0
       virtual packages : __osx=12.3=0
                          __unix=0=0
                          __archspec=1=arm64
       base environment : /Users/martin/mambaforge  (writable)
      conda av data dir : /Users/martin/mambaforge/etc/conda
  conda av metadata url : None
           channel URLs : https://conda.anaconda.org/conda-forge/osx-arm64
                          https://conda.anaconda.org/conda-forge/noarch
          package cache : /Users/martin/mambaforge/pkgs
                          /Users/martin/.conda/pkgs
       envs directories : /Users/martin/mambaforge/envs
                          /Users/martin/.conda/envs
               platform : osx-arm64
             user-agent : conda/4.10.3 requests/2.26.0 CPython/3.9.7 Darwin/21.4.0 OSX/12.3
                UID:GID : 501:20
             netrc file : None
           offline mode : False
```
</details>
