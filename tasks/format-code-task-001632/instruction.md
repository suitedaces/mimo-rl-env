when we patch the original `require` it becomes very hard to type tests.
i think we should move everything that is jest specific to `jest` object and have consistent type information for it

Concretely, things like `requireActual` (currently only on the patched `require`) should also be exposed on the `jest` object (e.g. `jest.requireActual(...)`).
