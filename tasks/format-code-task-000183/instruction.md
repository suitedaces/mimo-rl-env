## Problem Statement

When I want to add a custom variable to a particle in Parcels, right now I have to subclass `JITParticle` just to attach one extra `Variable`. It feels heavy when I only want one or two extra fields tracked per particle. Could the particle classes offer a class-level helper, in the requested `add_variable` style, that gives me back a pclass I can hand straight to `ParticleSet`? Would make my scripts so much cleaner.

## Expected outcomes

- Single custom variable: public particle classes such as `JITParticle` and `ScipyParticle` support `add_variable(...)` as a class-level API that returns a new particle class usable as `pclass` in `ParticleSet`.
- Variable configuration: the single-variable API supports adding a variable from either a variable name plus existing `Variable` configuration options, or an existing `Variable` definition, while preserving normal `Variable` semantics.
- Multiple custom variables: particle classes support adding more than one `Variable` definition in one class-level call, while preserving each variable's own name, initial value, dtype, and other supported configuration.
- ParticleSet integration: a `ParticleSet` constructed with a class returned by the new API can read and write the added variables during kernels in both JIT and Scipy particle modes where those modes are supported.
- Backward compatibility: the existing pattern of declaring custom `Variable`s in a particle subclass class body continues to work and remains behaviorally equivalent for the same variables.

## Implementation notes

- The public API shape is part of the requested behavior: `add_variable(...)` is the single-variable entry point, and a plural class-level entry point is expected for multiple variables.
- The concrete class-construction mechanism, internal registration strategy, generated class naming, validation location, and storage layout are implementation details.
- The new API should preserve existing `Variable` semantics rather than introducing a separate variable model.
- Keep existing subclass-based particle definitions compatible while adding the lighter-weight class-level entry points.
