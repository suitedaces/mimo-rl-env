`_matrix/client/unstable/org.matrix.msc2946/rooms/{roomId}/hierarchy` returns a next_batch string for spaces with more than 50 children as expected.
Pparsing the pagination token then only returns 11 rooms in my case, even though there should be much more. The Space in question has 135 space children.
Different spaces return different seemingly random numbers after the second call, but never the actual number.

**To Reproduce**
Steps to reproduce the behavior:

- call `_matrix/client/unstable/org.matrix.msc2946/rooms({roomId}/hierarchy` for a space with more than 50 children, ideally more than 100

- repeat the call and parse the next_batch string

- wrong number of spaces are returned

**Expected behavior**

- return actual number of spaces and if >50 another next_batch string

tested with v1.43.0
