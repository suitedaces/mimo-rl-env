Multiindex with single level no longer allows selecting columns
This works fine in pandas 0.22.0 but fails in 0.25.3 It appears a bug may have been introduced.

I have some old code that accidentally created a MultiIndex with a single level instead of a regular index, but everything worked fine with pandas 0.22.0. However, in new versions of pandas, that MultiIndex breaks pandas ability to select columns and gives an extremely misleading error message. In this case, I don't need the MultiIndex, so I can just remove that; but I think this code ought to work. (And it did work in the old 0.22.0 version).  

```
import numpy as np
import pandas as pd

names = ['FirstColumn', 'SecondColumn']
data = np.array([[5,6],[7,8]])
df = pd.DataFrame(data, columns = [names]) #Bug: the brackets around "[names]" creates a
#multi-index but that was unintentional. (It's still legal, though). 
#But "df.head()" and "df.describe()" both look normal so you can't see anything is wrong. 

#All of the following work as expected in 0.22.0 but give misleading errors in 0.25.3.
#These all work with a regular index, but the 0.25.3 MultIndex doesn't like it. 
df['FirstColumn'] #ERROR! 
df.FirstColumn #ERROR! 
df.loc[:,'FirstColumn'] #ERROR! 

#This works, but it shouldn't be necessary to do this. The above syntax is more standard.
df.xs('FirstColumn', axis=1, level=0)
```
Those failing statements give misleading errors about ```only integer scalar arrays can be converted to a scalar index```  but that code looks like it ought to work, and it did work fine in the previous versions of pandas. Can we make the standard methods of selecting columns work with the MultiIndex?
