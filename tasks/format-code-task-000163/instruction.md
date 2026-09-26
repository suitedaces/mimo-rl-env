## `SetAttributes` silently swallows wrong number of arguments

`SetAttributes` is supposed to take exactly two arguments (a symbol/list of symbols and an attribute/list of attributes), but if I call it with the wrong arity Mathics just returns the expression unevaluated without saying anything is wrong.

For example, I forgot to wrap multiple attributes in a list:

```
In[1]:= SetAttributes[f, Flat, Protected]
Out[1]= SetAttributes[f, Flat, Protected]

In[2]:= Attributes[f]
Out[2]= {}
```

No warning, no message — but obviously nothing was actually set, which is pretty confusing. Same thing if I just forget the second argument entirely:

```
In[3]:= SetAttributes[g]
Out[3]= SetAttributes[g]
```

Again, completely silent.

In WMA you get a message telling you the call had the wrong number of arguments (the usual "called with N arguments; 2 arguments are expected" style of complaint), which makes it immediately obvious what went wrong. Mathics should do the same for `SetAttributes` so that bad calls don't look like they succeeded.
