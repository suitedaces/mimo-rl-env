Creation of geodataframe shouldn't modify the original dataframe
I'm using geopandas 0.5.1 for the example. Creating a geodataframe from a Pandas dataframe modifies the input dataframe, even when the `geometry` is not a column of the input dataframe. This creates an issue especially when the same dataframe is used to create multiple geodataframes, in which case the first geometry definition would always prevail in subsequent operations.

````
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
df = pd.DataFrame({'Name':['Adam','Barbara','Cat','Doug','Ezra','Fiona','Greg'],
                  'lat':[35.5,35.2,34.89,36.1,35.78,35.76,34.99],
                  'lon':[-112.02,-111.09,-115.3,-114.01,-113.02,-112.9,-112.02]})
gdf = gpd.GeoDataFrame(df, geometry = [Point(x,y) for x, y in zip(df.lon,df.lat)])
print(gdf.columns)
>>> Index(['Name', 'lat', 'lon', 'geometry'], dtype='object')
print(df.columns)
>>> Index(['Name', 'lat', 'lon', 'geometry'], dtype='object')
````
