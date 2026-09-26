Incorrect requirements.txt formatting in poetry export
The `requirements.txt` format needs to put a space in front of the semicolon that specifies the package and the pyversion and platform constraints.  Right now, without the space, the semicolon will be interpreted as part of a URL.  See this issue in `packaging`:
https://github.com/pypa/packaging/issues/456
