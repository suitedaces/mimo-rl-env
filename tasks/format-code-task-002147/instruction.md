## `CylindricalMesh` / `SphericalMesh` centroids don't line up with cell vertices

I'm setting up a tally in OpenMC using a `CylindricalMesh` for a fuel region that's offset from the world origin, so I gave the mesh a non-zero `origin`. When I try to overlay the centroids of the mesh cells on the geometry (using `mesh.centroids`), they're clearly not in the right place — they don't sit at the centers of the cells implied by `mesh.vertices`.

Reproducer:

```python
import numpy as np
import openmc

mesh = openmc.CylindricalMesh(
    r_grid=[0.0, 0.5, 1.0],
    phi_grid=[0.0, np.pi, 2*np.pi],
    z_grid=[0.0, 1.0, 2.0],
    origin=(5.0, 0.0, 0.0),
)

verts = mesh.vertices
centroids = mesh.centroids

print("vertices:")
print(verts)
print("centroids:")
print(centroids)
```

The `vertices` look reasonable — Cartesian points sitting around x ≈ 5 like I'd expect. But the values coming back from `centroids` are nowhere near the midpoints of those vertices.

I'd expect `mesh.centroids` to give me the geometric center of each mesh cell, in the same Cartesian frame as `mesh.vertices` — i.e. the midpoints between adjacent vertices along each axis. With `RegularMesh` and `RectilinearMesh` that's exactly what I get, and `vertices` and `centroids` agree. It's only `CylindricalMesh` (and `SphericalMesh` — I tried it as a sanity check and saw the same thing) where the two don't line up.

Could the centroid computation for these two mesh types be fixed so that the output is consistent with `vertices` and respects the `origin` correctly?
