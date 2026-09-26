## Feature request: lookup an entry by its UUID

The current `find_entries_by_*` helpers all match against string fields (title, username, password, url, notes, path). I couldn't find anything that lets me look up an `Entry` by its UUID.

My use case: I have an external tool that stores references to KeePass entries by their UUID (since titles/usernames can change, UUIDs are the only stable identifier). When I read the database back with `PyKeePass`, I want to resolve those stored UUIDs back into the corresponding `Entry` objects so I can read the password, update notes, etc.

Right now the only workarounds I can think of are either iterating over `kp.entries` and comparing UUIDs by hand, or dropping down to raw XPath against the underlying tree — both feel like things `PyKeePass` should just expose directly, since UUID lookup is arguably the most natural way to address an entry.

Could we get a first-class "find entry by UUID" method on `PyKeePass`? Input would be the UUID as a normal string (the kind you'd get from `str(uuid.uuid4())` or copy out of another tool), and the output an `Entry`. I'd expect the method to be named something like `find_entry_by_uuid` (singular, since UUIDs are unique).
