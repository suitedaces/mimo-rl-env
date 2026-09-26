[ENH] Add `fill_value` and `explicit` parameters to `complete`
# Brief Description

<!-- Please provide a brief description of what you'd like to propose. -->

fill null values generated during `complete` and decide if existing nulls should be filled, or only nulls generated from the `complete` function. idea inspired by the updates to the [complete](https://tidyr.tidyverse.org/reference/complete.html) function in tidyr.

# Example API

```python
# source dataframe
df =  dict(
  group = (1,2, 1, 2),
item_id = (1,2, 2, 3),
 item_name = ("a", "a", "b", "b"),
value1 = (1, pd.NA, 3, 4),
 value2 = range(4,8)
 )

df  = pd.DataFrame(df)

   group  item_id item_name value1  value2
0      1        1         a      1       4
1      2        2         a   <NA>       5
2      1        2         b      3       6
3      2        3         b      4       7

# fill value and explicit set to True
df.complete('group', ('item_id', 'item_name'), fill_value = 0, sort = True, explicit = True) 

   group  item_id item_name  value1  value2
0      1        1         a       1     4
1      1        2         a       0     0
2      1        2         b       3     6
3      1        3         b       0     0
4      2        1         a       0     0
5      2        2         a       0     5
6      2        2         b       0     0
7      2        3         b       4     7

df.complete('group', ('item_id', 'item_name'), fill_value = 0, sort = True, explicit = False) 

   group  item_id item_name  value1  value2
0      1        1         a       1     4
1      1        2         a       0     0
2      1        2         b       3     6
3      1        3         b       0     0
4      2        1         a       0     0
5      2        2         a    <NA>     5
6      2        2         b       0     0
7      2        3         b       4     7
``` 

It is easy to do a `fillna` after `complete`; however it looks cumbersome filling only the nulls generated from the `complete` function. I'll gladly take suggestions for filling only the null values without adding new parameters.
