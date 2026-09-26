# Problem Statement

I'm working with `Hyperplane` and `Line2D` in LazySets, and I want to be able to generate random points that actually lie on the hyperplane/line. Right now if I just call `sample` on a `Hyperplane`, the points I get aren't on it. It'd also be handy to have a way to project an arbitrary point onto a hyperplane or line. Ideally sampling a hyperplane would just give me points on it by default, but I'd still like to control the underlying distribution if I want to.

# Expected outcomes

- Projection onto hyperplane-like sets:
  - `project(x, hp::Hyperplane)` should accept an arbitrary point and return its orthogonal projection onto the given hyperplane.
  - The returned point should lie on the target hyperplane, and points that are already on the hyperplane should be unchanged up to the numeric precision of the element type.
- Projection onto two-dimensional lines:
  - `project(x, L::Line2D)` should accept an arbitrary two-dimensional point and return its orthogonal projection onto the given line.
  - The returned point should lie on the target line, and points that are already on the line should be unchanged up to the numeric precision of the element type.
- Sampling from hyperplanes and lines:
  - Calling `sample` on a `Hyperplane` without specifying a sampler should produce points that lie on that hyperplane.
  - Calling `sample` on a `Line2D` without specifying a sampler should produce points that lie on that line.
  - `HyperplaneSampler` should be available as a sampler for both `Hyperplane` and `Line2D`, and samples produced with it should lie on the requested set.
  - `HyperplaneSampler` should work with its default configuration and should also allow callers to control the sampling distribution through its public API.

# Implementation notes

- Preserve the existing public sampling API style and numeric-type flexibility used elsewhere in LazySets.
- The concrete implementation strategy, helper organization, and validation location are up to the implementer, as long as the externally observable projection and sampling behavior above is satisfied.
- Tests should tolerate ordinary floating-point roundoff for inexact numeric types.
