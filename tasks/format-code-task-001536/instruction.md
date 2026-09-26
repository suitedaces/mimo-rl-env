## Missing Go bindings for several OpenCV core array functions

I'm using gocv to do some image/matrix processing in Go, and there are a number of standard OpenCV core array functions that I'd expect to be available but currently aren't exposed in the Go API.

For comparison, gocv already wraps things like `ExtractChannel`, `DFT`, `InRange`, `MeanStdDev`, `Multiply`, `Normalize`, etc. — but a bunch of equally common ones from the same OpenCV module (`core_array`) are missing. Right now I either have to do the work in another language and shuttle data across, or write my own cgo wrapper for each one, which kind of defeats the purpose of using the binding.

The ones I keep running into and would love to see added:

- `FindNonZero` — get the locations of all non-zero pixels in a Mat (super useful after thresholding/masking)
- `Flip` — flip a 2D array horizontally / vertically / both
- `Gemm` — generalized matrix multiplication
- `Hconcat` — horizontal concatenation of two matrices
- `Idct` — inverse discrete cosine transform (the `DCT` wrapper is already there, but no inverse)
- `Idft` — inverse discrete Fourier transform (same situation — `DFT` is there but no inverse)
- `InsertChannel` — insert a single channel into a multi-channel Mat (the inverse of the existing `ExtractChannel`)
- `Invert` — matrix inverse / pseudo-inverse
- `Log` — element-wise natural log (the `Exp` wrapper is there, but no `Log`)
- `Magnitude` — magnitude of 2D vectors from x/y components
- `Max` — per-element max of two arrays

These are all standard `cv::` functions in the OpenCV C++ API and have direct equivalents in the Python bindings, so they should be straightforward to wrap following the same pattern as the existing `core` functions in gocv. Could these be added to the `core` package?
