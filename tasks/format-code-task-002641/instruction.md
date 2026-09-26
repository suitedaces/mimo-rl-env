display_genotypes ValueError
I'm trying to display the genotypes in the Hail tutorial's [1kg.vcf.bgz](https://storage.googleapis.com/hail-tutorial/1kg.vcf.bgz).

```
import xarray as xr
import sgkit as sg

sg.io.vcf.vcf_to_zarr("https://storage.googleapis.com/hail-tutorial/1kg.vcf.bgz", "1kg.zarr")
ds = xr.open_zarr("1kg.zarr")
sg.display_genotypes(ds, max_variants=8, max_samples=8)
```

When I run the above code, I die at https://github.com/pystatgen/sgkit/blob/master/sgkit/display.py#L182 with `ValueError: Index contains duplicate entries, cannot reshape`.

I'm probably doing something wrong, but I was a little surprised to get this error.

In case it matters, when I use the suggested code from the getting started guide, the genotype array prints just fine:

```
(ds.call_genotype[:5, :5].to_series()
    .unstack().where(lambda df: df >= 0, None).fillna('.')
    .astype(str).apply('/'.join, axis=1).unstack())
```
