## Device removal aborts when a brick on the device has no path, leaving the device stuck

I'm trying to decommission a disk from one of my nodes using the normal flow — set the device offline and then transition it to the failed state so heketi will move the bricks off it automatically.

On most devices this works fine. But I have one device where the operation stops partway through with an error, and after that:

- the device is still in the offline state (it didn't transition to failed),
- only some of the bricks on it got migrated; the rest are still associated with the device,
- so I can't actually retire the disk.

When I look at the device info via the API, I notice that a few of the bricks on this device have an empty `path` field. As far as I can tell these are leftovers from an earlier operation that didn't complete cleanly — the brick entries exist in heketi's DB but there's nothing real backing them on the host (no LV, nothing under `/var/lib/heketi/mounts/...`). The bricks that do have a proper path migrate just fine; it's the empty-path ones that seem to trip up the whole remove.

The only way I've found to get unstuck is to manually edit the heketi DB to drop those phantom brick entries and then re-run the remove, which is not something I want to be doing on a production cluster.

It would be much better if `Remove` on a device just skipped bricks that obviously can't be migrated (no path = nothing to move anyway) and kept going with the rest, so the device can actually reach the failed state. A warning in the log naming which brick got skipped would be enough for me to follow up on the stale entries afterwards.
