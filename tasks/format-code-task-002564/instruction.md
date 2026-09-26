## salt.utils.vmware: no companion helper to disconnect from a vCenter / ESXi service instance

`salt.utils.vmware.get_service_instance(...)` gives me a connected service
instance to talk to a vCenter server or ESXi host, and the rest of the
module exposes a consistent set of helpers around it (`list_clusters`,
`list_datastores`, `wait_for_task`, ...). All of those helpers wrap any
underlying pyVmomi failures into Salt's own exception types
(`VMwareApiError`, `VMwareRuntimeError`), which is what the rest of my
code is set up to catch.

The thing I'm missing is the other half of the lifecycle: a way to
explicitly close the connection to the service instance from
`salt.utils.vmware` itself.

Today the only options I have are:

- rely on the `atexit`-registered cleanup that happens inside
  `_get_service_instance`, which only fires at interpreter shutdown — not
  useful when I want to release the session sooner (long-running proxy
  minions, repeated reconnects against different vCenters in one
  process, tests that set up and tear down sessions, etc.); or
- reach into pyVmomi directly and call `pyVim.connect.Disconnect(si)`
  myself. That works, but now my code

  1. has to import pyVmomi internals directly instead of going through
     `salt.utils.vmware`, and
  2. raises raw `vim.fault.VimFault` / `vmodl.RuntimeFault` on failure,
     which is inconsistent with everything else in this module — the rest
     of my error handling around vmware utils catches the Salt-level
     exceptions.

It would be great if `salt.utils.vmware` provided a disconnect counterpart
to `get_service_instance` so that connection teardown goes through the
same module and surfaces failures using the same Salt exception types as
the rest of the helpers there.
