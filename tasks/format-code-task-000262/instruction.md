## Problem Statement

I often need to cap MRI intensity values before the rest of my preprocessing, but I don’t see a built-in TorchIO transform for just clipping a ScalarImage to fixed lower/upper limits. It would be nice if I could use this like the other intensity transforms, including cases where I only want to set one side of the clamp.

## Expected outcomes

- A public `Clamp` intensity transform is available through the usual TorchIO transform APIs, including `torchio.Clamp` and `torchio.transforms.Clamp`.
- `Clamp` can be instantiated with optional `out_min` and `out_max` keyword arguments, while still accepting the common transform options used by other TorchIO transforms.
- When applied to scalar intensity images, `Clamp` caps values below the configured lower limit to that lower limit, caps values above the configured upper limit to that upper limit, and leaves values already within the configured range unchanged.
- `Clamp` supports one-sided use: specifying only `out_min` applies only the lower cap, and specifying only `out_max` applies only the upper cap.
- The preprocessing transforms documentation lists `Clamp` alongside the other intensity preprocessing transforms.

## Implementation notes

- Follow the conventions of existing TorchIO intensity preprocessing transforms for public API exposure, subject/image handling, and transform options.
- The internal organization, helper methods, validation location, and exact implementation mechanism are up to the implementer, as long as the observable behavior above is satisfied.
