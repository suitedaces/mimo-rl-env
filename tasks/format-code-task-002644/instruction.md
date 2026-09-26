docs update needed for reg_proj
Just so we don't forget. I hit an issue with our online example using min=(),max =()  in `reg_proj` shown here:
`reg_proj(g.ampl, b.ampl, min=(0, 1e-4), max=(0.2, 5e-4),
    ...          nloop=(51, 51), id='core', otherids=['jet'])`

This creates an error:
```
reg_proj(b1.r0, b1.beta, min=(0,0), max=(200,10), nloop=(50,50))
..
TypeError: 'tuple' object does not support item assignment
```

The working syntax:
`reg_proj(b1.r0, b1.beta, min=[0,0], max=[150,10], nloop=(50,50))`

The help doc needs a review and updating.
