I'm seeing inconsistent positional-argument deprecation behavior in `scipy.sparse.linalg`: calls like `cg(A, b, x0)` trigger a warning about positional args, but `gcrotmk`, `lgmres`, `minres`, and `tfqmr` let later options like `tol`, `maxiter`, `M`, or `shift` be passed positionally without any warning. `inspect.signature` also shows those later options as regular positional-or-keyword parameters for some of these solvers, which doesn't line up with the deprecation warnings I'm getting elsewhere.

Expected outcomes:
- Sparse iterative solvers apply a consistent public positional-argument deprecation boundary: `x0` remains accepted as the third positional argument, while later solver options are treated as keyword-only for deprecation purposes.
- Calls that pass compatible solver options after `x0` positionally continue to execute for backwards compatibility, but emit a `DeprecationWarning`.
- Public Python introspection for the affected solvers reflects the same boundary: users can see `x0` as positionally accepted and later solver options as keyword-only.

Implementation notes:
- Preserve existing numerical solver behavior and backwards-compatible execution of currently accepted calls while aligning warning behavior and public signatures.
- The exact implementation mechanism and internal organization are left to the implementer, as long as the public call behavior, warnings, and inspected signatures match the outcomes above.
