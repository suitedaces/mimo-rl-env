## Problem Statement

I'm using `osutil.EnsureFileState` in snapd to keep some files in sync with their desired state, and it works great for regular file content, but I've got a case where what I actually want to manage is a symlink pointing at a specific target. Right now there doesn't seem to be a way to express "this path should be a symlink to X" through EnsureFileState — I end up having to drop down and manage the symlink manually outside of it, which is annoying because I lose the same "create if missing, fix if drifted, no-op if already correct" behavior I get for regular files. Could we get symlinks supported as a FileState too, so I can hand EnsureFileState a target and let it do the right thing?

## Expected outcomes

- Symlink desired state:
  - `osutil.SymlinkFileState` should be available as a `FileState` implementation for describing a symbolic link target.
  - Calling `State()` on `osutil.SymlinkFileState{Target: target}` should represent the requested link target as a symlink state.

- Ensuring symlinks:
  - `osutil.EnsureFileState` should accept a symlink `FileState` and create the requested symlink when the path is missing.
  - If the path already is a symlink to the requested target, `osutil.EnsureFileState` should report `osutil.ErrSameState`.
  - If the path exists but does not match the requested symlink target, `osutil.EnsureFileState` should update it so that it points to the requested target.
  - Symlink states should also work when used through directory-state synchronization APIs that accept `FileState` values.

- Unsupported file-state kinds:
  - `osutil.EnsureFileState` should reject `FileState` implementations that report neither a regular-file state nor a symlink state, with an internal-error message indicating that the reported type is unsupported.
  - Existing built-in regular-file `FileState` implementations should reject non-regular modes with an internal-error message indicating that only regular files are supported.

## Implementation notes

The concrete comparison and update strategy is up to the implementation, as long as the externally observable filesystem state and errors match the outcomes above. Keep existing regular-file behavior intact while adding symlink support and validation for unsupported state kinds.
