`selector` should accept integers and strings, for all functions accepting the `selector` argument
Example functions are `update_trace`, `for_each_shape`, etc.

If the `selector` keyword argument is an integer, it should behave as follows:
 - If row and col aren't specified, it should act as an index into `fig.data`, i.e., `fig.data[selector]`
 - If they are, then it acts as an index into the objects on that subplot, e.g., `list(fig.select_traces(row=r,col=c))[selector])`

If the `selector` keyword argument is a string, it should create a dictionary whose sole key is `type` and `selector` is the value at the key, e.g., `if type(selector) == type(str()): selector = dict(type=selector)`.
