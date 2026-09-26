add_lines behaves different than documentation suggests
### Describe the bug, what's wrong, and what you expected.

[The documentation of `add_lines` ](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.add_lines.html) states that an array of points like `np.array([[0, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 0]])` adds two line segments, probably from point 0 to point 1 and from point 2 to point 3.
However, three line segments are added, one between each point in the sequence. It behaves like `lines_from_points` which it should not according to documentation.

### Steps to reproduce the bug.

This is the example of the docu:
```python
import numpy as np
import pyvista
pl = pyvista.Plotter()
points = np.array([[0, 1, 0], [1, 0, 0], [1, 1, 0], [2, 0, 0]])
actor = pl.add_lines(points, color='yellow', width=3)
pl.camera_position = 'xy'
pl.show()
```

### System Information

```shell
--------------------------------------------------------------------------------
  Date: Thu Dec 01 11:12:36 2022 CET

                OS : Linux
            CPU(s) : 40
           Machine : x86_64
      Architecture : 64bit
               RAM : 62.8 GiB
       Environment : IPython
       File system : ext4
       GPU Details : error

  Python 3.8.10 (default, Jun 22 2022, 20:18:18)  [GCC 9.4.0]

           pyvista : 0.37.0
               vtk : 9.2.2
             numpy : 1.23.5
           imageio : 2.22.4
            scooby : 0.7.0
             pooch : v1.6.0
        matplotlib : 3.6.2
           IPython : 7.13.0
             scipy : 1.9.3
              tqdm : 4.64.1
--------------------------------------------------------------------------------
```


### Screenshots

_No response_
