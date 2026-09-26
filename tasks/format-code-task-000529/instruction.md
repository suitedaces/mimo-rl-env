Error when trying to fix a model
Hi, Bashtage:

I have a problem when I'm trying to `fix` a model. The use case I'm going after is to fit a model, store the parameters on disk and load it again to build a model using `fix`. But when I try that I get the error:

```
  File "/usr/local/lib/python3.6/site-packages/arch/univariate/base.py", line 322, in fix
    resids = self.resids(self.starting_values())
  File "/usr/local/lib/python3.6/site-packages/arch/univariate/base.py", line 567, in starting_values
    params = np.asarray(self._fit_no_arch_normal_errors().params)
  File "/usr/local/lib/python3.6/site-packages/arch/univariate/mean.py", line 538, in _fit_no_arch_normal_errors
    nobs = self._fit_y.shape[0]
AttributeError: 'NoneType' object has no attribute 'shape'
```

Simple code to reproduce is this:

```python
import datetime as dt
import pandas_datareader.data as web

import arch

st = dt.datetime(1990, 1, 1)
en = dt.datetime(2016, 1, 1)

data = web.get_data_yahoo('^GSPC', start=st, end=en)
returns = 100 * data['Adj Close'].pct_change().dropna()

result = arch.arch_model(returns).fit()
fixed_result = arch.arch_model(returns).fix(result.params)
```

It this a supported usecase?
