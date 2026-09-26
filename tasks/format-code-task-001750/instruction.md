CUDA<->CPU interface for 3D
Continuation of the discussion from #122. It would be good to have a way to set the `Scattering3D` object to CPU or CUDA modes, just like the 1D and 3D codes with `cpu()` and `cuda()` functions that mutate the object. Note that calling `cuda()` doesn't have to make the object move its filters to GPU (like the 1D and 2D code currently does), but simply gives it the option to. This may be better in 3D due to the memory constraints.

Right now, all this could do is throw and error if the input to `forward()` is not compatible (i.e., sending a CPU tensor to a `Scattering3D` object that is in CUDA mode, or vice versa), but it unifies the interfaces and allows for more complex behavior in the future.
