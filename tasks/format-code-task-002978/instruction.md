[BUG] Setting pml sizes in 2D
**Describe the bug**
It is not possible to set `pml_x_size` and `pml_y_size` using a two-item list `pml_size`. Instead only the first value is taken. 

This is not the case for 3D simulations.

**Expected behavior**
I'd expect that the pml lengths in x and y are assigned from both entries in the list `pml_size`
