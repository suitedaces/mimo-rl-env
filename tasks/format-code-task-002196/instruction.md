BUG: pd.crosstab cannot handle series with the same name
the following works fine

> > > c = pd.Series(rand(3))
> > > pd.crosstab(c,c)

however, when giving the series a name, it fails:

> > > c.name='test'
> > > pd.crosstab(c,c)

Traceback (most recent call last):
  File "C:\Python35\Lib\site-packages\pandas\indexes\multi.py", line 515, in _get_level_number
    'level number' % level)
ValueError: The name test occurs multiple times, use a level number

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<pyshell#56>", line 1, in <module>
    pd.crosstab(c,c)
  File "C:\Python35\Lib\site-packages\pandas\tools\pivot.py", line 462, in crosstab
    aggfunc=len, margins=margins, dropna=dropna)
  File "C:\Python35\Lib\site-packages\pandas\tools\pivot.py", line 127, in pivot_table
    table = agged.unstack(to_unstack)
  File "C:\Python35\Lib\site-packages\pandas\core\frame.py", line 3946, in unstack
    return unstack(self, level, fill_value)
  File "C:\Python35\Lib\site-packages\pandas\core\reshape.py", line 398, in unstack
    return _unstack_multiple(obj, level)
  File "C:\Python35\Lib\site-packages\pandas\core\reshape.py", line 252, in _unstack_multiple
    clocs = [index._get_level_number(i) for i in clocs]
  File "C:\Python35\Lib\site-packages\pandas\core\reshape.py", line 252, in <listcomp>
    clocs = [index._get_level_number(i) for i in clocs]
  File "C:\Python35\Lib\site-packages\pandas\indexes\multi.py", line 519, in _get_level_number
    raise KeyError('Level %s not found' % str(level))
KeyError: 'Level test not found'

The use case for having series with the same name is e.g. where you want to crosstab data selected from a dataframe with a multi index. For example: c1 = mydf.xs(val1).mycolumn and c2 = mydf.xs(val2).mycolumn and then you want to do pd.crosstab(c1,c2). This will produce the error as in the simple example above.
