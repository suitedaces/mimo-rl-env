## Uploading a DataFrame with non-ASCII text fails

I have a pandas DataFrame with some string columns containing accented characters (Spanish place names like `"Málaga"`, `"A Coruña"`, plus a few rows with Asian characters). I'm trying to push it to CARTO with something along the lines of:

```python
from cartoframes.data import Dataset

ds = Dataset(df)
ds.upload(table_name='my_places', credentials=creds, if_exists='replace')
```

The DataFrame itself looks fine in pandas (the strings display correctly, no weird mojibake), but the upload blows up partway through instead of finishing. If I strip the rows that contain accented / non-ASCII characters and re-run with the same code path, everything uploads without complaint, so it seems specific to non-ASCII content in the data.

I'd expect `Dataset.upload` to handle arbitrary unicode text in string columns — having to pre-sanitize / drop rows with accents before every upload is pretty painful when the whole point of the dataset is Spanish-speaking locations.
