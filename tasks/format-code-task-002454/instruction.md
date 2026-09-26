Textures don't appear if init'ed from numpy array with dtype not being `np.uint8` while using pythreejs backend
### Describe the bug, what's wrong, and what you expected.

There seems to be an issue with plotting textures using a pythreejs backend when initialized using `pvvista.numpy_to_texture(img)` where `img` is a numpy array that does _not_ have dtype `np.uint8`. When setup as such, the plot always shows a mesh with a black texture. It would be helpful to others to either mention in the docs that `numpy_to_texture()` expects the input to have dtype `np.uint8` and/or to show a warning when using a float texture array with a pythreejs backend. 

### Steps to reproduce the bug.

In a Jupyter notebook, run:

```python 
import pyvista as pv
import numpy as np

pv.set_jupyter_backend('pythreejs')

mesh = pv.read('example_mesh.obj')
tex_im = np.ones((1024, 1024, 3)) * 255.
tex = pv.numpy_to_texture(tex_im)

mesh.plot(texture=tex) # this doesn't work (shows black texture)
 ```
However, with the proper dtype, it works fine

```python
import pyvista as pv
import numpy as np

pv.set_jupyter_backend('pythreejs')

mesh = pv.read('example_mesh.obj')
tex_im = np.ones((1024, 1024, 3), dtype=np.uint8) * 255
tex = pv.numpy_to_texture(tex_im)

mesh.plot(texture=tex) # this works fine (shows a white texture)
```

### System Information

```shell
--------------------------------------------------------------------------------
  Date: Wed Aug 03 13:56:49 2022 EDT

                OS : Linux
            CPU(s) : 16
           Machine : x86_64
      Architecture : 64bit
       Environment : Jupyter
       GPU Details : error

  Python 3.8.13 (default, Mar 28 2022, 11:38:47)  [GCC 7.5.0]

           pyvista : 0.35.2
               vtk : 9.1.0
             numpy : 1.22.3
           imageio : 2.9.0
           appdirs : 1.4.4
            scooby : 0.5.12
        matplotlib : 3.5.2
           IPython : 8.3.0
        ipyvtklink : 0.2.2
             scipy : 1.7.2
              tqdm : 4.64.0
            meshio : 5.3.4
        jupyterlab : 3.3.2
         pythreejs : Version unknown

  Intel(R) oneAPI Math Kernel Library Version 2021.4-Product Build 20210904
  for Intel(R) 64 architecture applications
--------------------------------------------------------------------------------
```


### Screenshots

_No response_
