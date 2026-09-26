csvlook 1.0: Are there options to render and output the complete data?
csvlook 1.0 truncates rows, columns, and fieldwidth -- to 20, 6, and 20, respectively -- by default...and there doesn't seem to be an option via the csvlook interface to bypass that. 

Proposed change: Go back to 0.9.1 behavior, in which the entire table was rendered, leaving it up to the user to control column/row dimensions with `head` and `csvcut` before piping into `csvlook`.

(note: that reading from stdin doesn't currently work in 1.0 https://github.com/wireservice/csvkit/issues/623)

Here's an example of row, column, and fieldwidth truncation in csvlook 1.0:

``` sh
$ csvlook examples/realdata/ks_1033_data.csv

|--------+----------+--------+------------------+----------------------+----------+------|
|  state | county   |   fips | nsn              | item_name            | quantity | ...  |
|--------+----------+--------+------------------+----------------------+----------+------|
|  KS    | ALLEN    | 20,001 | 1005-00-073-9421 | RIFLE,5.56 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-073-9421 | RIFLE,5.56 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-073-9421 | RIFLE,5.56 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-073-9421 | RIFLE,5.56 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-073-9421 | RIFLE,5.56 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-589-1271 | RIFLE,7.62 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-589-1271 | RIFLE,7.62 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-589-1271 | RIFLE,7.62 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-589-1271 | RIFLE,7.62 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-589-1271 | RIFLE,7.62 MILLIM... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ALLEN    | 20,001 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  KS    | ANDERSON | 20,003 | 1005-00-589-1271 | RIFLE,7.62 MILLIM... |        1 | ...  |
|  KS    | ANDERSON | 20,003 | 1005-00-726-5655 | PISTOL,CALIBER .4... |        1 | ...  |
|  ...   | ...      |    ... | ...              | ...                  |      ... | ...  |
|--------+----------+--------+------------------+----------------------+----------+------|
```
