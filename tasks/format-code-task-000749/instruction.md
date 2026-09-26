## Problem Statement

我在给 daos 写一个新的 test SConscript，需要用 mpicc 编一部分东西，但又不想让所有用 base_env 的子模块都被强行塞上 mpicc 的路径——现在基础环境在初始化时会被加入 MPI 编译器相关 PATH，我没法拿到一个"干净的 base_env"，也没法单独 Import 一个配好 MPI 的环境。能不能把这俩拆开，让 base_env 保持基础环境，再单独给我一个配好 MPI 的环境可以 Import？顺便如果机器上根本没装 mpich/openmpi，最好 scons 跑的时候能明确提示一下要跳过，不然现在静默不动我都不知道是没生效还是配漏了。

## Expected outcomes

- Environment export behavior:
  - SConscripts must be able to `Import('base_env_mpi')` in addition to the existing exported build environments.
  - When MPI is available for a normal build, `base_env_mpi` should be usable by MPI-dependent SConscripts as an MPI-capable environment.
  - When MPI is not available for a normal build, `base_env_mpi` should be `None` so MPI-dependent SConscripts can skip themselves through that public convention.
  - `base_env` should remain the non-MPI base environment, so SConscripts that only import and use `base_env` are not forced to inherit MPI compiler PATH changes.

- MPI-unavailable behavior:
  - During normal builds, if MPI cannot be found or configured, the build output should clearly state that MPI-dependent tests are being skipped.
  - The user-facing output should include the guidance strings `Skipping compilation for tests that need MPI` and `Install and load mpich or openmpi`.
  - MPI-dependent test build logic should be able to skip itself by observing that `base_env_mpi` is `None`.

- MPI-available behavior:
  - When MPI is available, MPI-dependent SConscripts should be able to use MPI without changing the observable environment of `base_env`.
  - Existing non-MPI build paths should continue to use `base_env` without requiring MPI-specific setup.

## Implementation notes

The exact placement of the MPI configuration logic and the way SConscripts organize their local environments are up to the implementer. Prefer behavior-preserving changes for non-MPI build paths, and avoid coupling unrelated submodules to MPI-specific environment changes.
