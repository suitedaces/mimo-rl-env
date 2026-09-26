# Add a point Jacobian to the public API

MJWarp can already do forward kinematics and reproduce MuJoCo's center-of-mass
quantities (`subtree_com`, `cdof`, etc.), but there is no way to ask "how does
each degree of freedom move a given point in the world?". MuJoCo exposes this as
`mj_jac`, and we want the equivalent in MJWarp so downstream code (end-effector
control, contact handling, custom constraints) can build on it.

Add a new public function `jac` to the package so that

```python
jacp, jacr = mujoco_warp.jac(m, d, point, body)
```

computes the translational (`jacp`) and rotational (`jacr`) Jacobians of a global
point that is attached to a body.

Contract:

- `m` and `d` are the usual MJWarp `Model` / `Data`. `point` is a Warp array of
  shape `(nworld, 3)` and float32 dtype holding the point's global coordinates in
  each world. `body` is an `int` body id.
- The call returns two Warp arrays `jacp` and `jacr` of float32 values whose
  `numpy()` representation has shape `(nworld, m.nv, 3)`. `jacp[w, i]` is the
  3-vector giving the contribution of degree of freedom `i` to the point's
  linear velocity in world `w`, and `jacr[w, i]` its contribution to the point's
  angular velocity. (This is the transpose of MuJoCo's `3 x nv` layout: column
  `i` of MuJoCo's Jacobian equals `jac[w, i]`.)
- A degree of freedom only influences the point when its body lies on the
  kinematic path between the world and `body` (i.e. `body` is in the subtree of
  the dof's body). Degrees of freedom that do not influence `body` must yield a
  zero 3-vector in both `jacp` and `jacr`. In particular, asking for the
  Jacobian of the world body (`body == 0`) yields all-zero arrays.
- Results must match MuJoCo's `mj_jac` for the same model, data and point, and
  must be computed independently per world so the function works for batched
  data (`nworld > 1`).

The function should run as warp kernels (no Python-side per-dof loops over the
data) and follow the conventions of the existing support utilities.
