I want `sinon.mock()` and `sinon.sandbox.mock()` to verify chained Mongoose expectations all the way down.

For a chain like `sinon.mock(Book).expects('update').chain('sort').chain('exec')`, calling `bookMock.verify()` should also verify the chained mock created for `sort()`. If `book.update(...).exec()` runs but `sort()` never happens, `verify()` should fail with the chained expectation error instead of treating the top-level expectation as enough.

The same recursive check should happen when sandboxed mocks are verified through `sinon.verify()`. Missing inner chain calls should surface as verification failures on the chained expectation, not as a successful top-level verify.
