## virtio-scsi controller doesn't respect the `useTransitionalVirtio` flag

I'm running some older guest workloads that need transitional virtio devices, so I'm setting `useTransitionalVirtio` on my VMIs. For most of my devices this works as I'd expect — when I look at the libvirt domain KubeVirt produces, my virtio NIC, the virtio-serial console, virtio-rng, the virtio disks, etc. all come out with the transitional model.

However, when my VMI has a SCSI disk and KubeVirt automatically adds a virtio-scsi controller for it, that controller's model is not affected by the flag at all. It always gets the same default model regardless of how I set `useTransitionalVirtio`. So I end up with a mixed domain where everything else honors the flag except the SCSI controller, and the flag effectively doesn't give me a fully transitional virtio domain.

This feels like an oversight from when the flag was introduced — the SCSI controller is also a virtio device and should follow the same rule as the rest of the virtio devices on the VMI.
