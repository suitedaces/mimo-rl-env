# Unified node CRUD on the folder-tree service

The folder-tree service holds the explorer's file/folder hierarchy in its state under
`folderTree.data`. That value is a list of root-folder nodes; every node may carry a
`children` list of nested nodes, and each node has a numeric `id`, a `name`, and a
`fileType` of `File`, `Folder`, or `RootFolder`.

Right now there is no convenient, general-purpose way to look up or mutate an arbitrary node
in that hierarchy — callers have to reach for several narrow helpers and reimplement tree
traversal themselves. Add a small, unified set of node operations to the service so that
consumers can manage the tree through one consistent API:

- **get** — given a node id, return the matching node from anywhere in the hierarchy
  (any root, at any depth). Return `null` when no node has that id.

- **add** — insert a new node.
  - When given a reference id that points to a **folder** (a `Folder` or `RootFolder`),
    the new node becomes a child of that folder.
  - When given a reference id that points to a **file**, the new node is placed alongside
    it, inside the same parent folder.
  - When called without a reference id, the new node is added as a new top-level root entry
    (appended after any existing roots).

- **update** — given a node carrying an `id` plus any fields to change, merge those fields
  into the existing node in place, leaving the node's other fields and its position in the
  tree untouched. Do nothing if no node has that id.

- **remove** — given a node id, delete that node (and its entire subtree) from the
  hierarchy. Sibling nodes are unaffected. Do nothing if no node has that id.

After any of `add`, `update`, or `remove`, the change must be reflected in the service's
state, so a subsequent **get** (and reading `folderTree.data`) observes it.

These operations work across a hierarchy that may contain multiple root folders and
arbitrarily nested children.
