## Problem Statement

I'm trying to set up unit tests for the value transfer tangle package and it's a pain that everything wants a real BadgerDB instance to construct things like `tangle.New` and `branchmanager.New`. My tests keep creating temp directories and leaving badger files on disk just to exercise some logic. Could we make these take a more generic store interface instead of requiring a concrete `*badger.DB`, so I could plug in an in-memory backend for tests and dev? Ideally I'd just hand it some in-memory kvstore and not touch the filesystem at all.

## Expected outcomes

- Value transfer tangle construction should no longer require callers to provide a concrete Badger database; callers should be able to construct it with a generic key-value store suitable for in-memory tests.
- Value transfer branch manager construction should no longer require callers to provide a concrete Badger database; callers should be able to construct it with the same kind of generic key-value store.
- Existing storage-backed test and development paths related to these components should be able to run against in-memory key-value storage without setting up temporary Badger directories or files, while preserving their existing observable behavior.

## Implementation notes

- Keep the storage backend choice abstract at package boundaries; persistent and in-memory backends should be interchangeable from the perspective of callers that only need key-value storage behavior.
- Do not remove or weaken existing value-transfer, branch-manager, tangle, or message-construction behavior; the change is about decoupling those paths from a concrete filesystem-backed database requirement.
