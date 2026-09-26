`highly_variable_genes()` with `flavor="cell_ranger"` fails there are less normalized dispersions than `n_top_genes`
- [x] I have checked that this issue has not already been reported.
- [x] I have confirmed this bug exists on the latest version of scanpy.
- [ ] (optional) I have confirmed this bug exists on the master branch of scanpy.

---

If there are very few genes some of the bins in `sc.pp.highly_variable_genes(adata, n_top_genes=1000, flavor="cell_ranger")` can contain a single gene leading to `NaN` values in the normalized expression vector which are removed here https://github.com/scverse/scanpy/blob/9018e16cae6f3199f914f58841b00a00790cd494/scanpy/preprocessing/_highly_variable_genes.py#L261. If after this filtering the dispersion vector is shorter then than `n_top_genes` there is an indexing error when selecting the dispersion cutoff here https://github.com/scverse/scanpy/blob/9018e16cae6f3199f914f58841b00a00790cd494/scanpy/preprocessing/_highly_variable_genes.py#L268. There should probably be a check (with a warning) when this happens.

### Minimal code sample (that we can copy&paste without having any data)

```python
import anndata
import numpy as np
import scanpy as sc

adata = anndata.AnnData(np.random.poisson(2, (100, 30)))
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=1000, flavor="cell_ranger")
```

```pytb
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.8/site-packages/scanpy/preprocessing/_highly_variable_genes.py", line 434, in highly_variable_genes
    df = _highly_variable_genes_single_batch(
  File "/usr/local/lib/python3.8/site-packages/scanpy/preprocessing/_highly_variable_genes.py", line 268, in _highly_variable_genes_single_batch
    disp_cut_off = dispersion_norm[n_top_genes - 1]
IndexError: index 29 is out of bounds for axis 0 with size 21
```

#### Versions

<details>

-----
anndata     0.7.8
scanpy      1.9.1
-----
PIL                 9.1.0
beta_ufunc          NA
binom_ufunc         NA
cffi                1.15.0
colorama            0.4.4
cycler              0.10.0
cython_runtime      NA
dateutil            2.8.2
defusedxml          0.7.1
google              NA
h5py                3.6.0
hypergeom_ufunc     NA
igraph              0.9.9
joblib              1.1.0
kiwisolver          1.4.2
llvmlite            0.38.0
louvain             0.7.1
matplotlib          3.5.1
mpl_toolkits        NA
natsort             8.1.0
nbinom_ufunc        NA
numba               0.55.1
numpy               1.21.5
packaging           21.3
pandas              1.4.2
pkg_resources       NA
psutil              5.9.0
pyparsing           3.0.8
pytz                2022.1
scipy               1.8.0
session_info        1.0.0
six                 1.16.0
sklearn             1.0.2
statsmodels         0.13.2
texttable           1.6.4
threadpoolctl       3.1.0
typing_extensions   NA
wcwidth             0.2.5
yaml                6.0
-----
Python 3.8.13 (default, Apr  7 2022, 04:56:26) [GCC 10.2.1 20210110]
Linux-5.10.76-linuxkit-x86_64-with-glibc2.2.5
-----
Session information updated at 2022-04-11 12:44

</details>
