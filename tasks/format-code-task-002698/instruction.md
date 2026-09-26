最近在 Windows 上用 spack 的 `install_tree`/`copy_tree` 拷一棵带 symlink 的目录树老出问题——源树里有些 symlink 指向的目标也在同一棵树里，结果复制时链接没有被正确保留下来；另外 junction 在我们这边也是当符号链接用的，但被这俩函数当成普通目录硬拷了一份，行为很奇怪。能不能加个参数让我自己控制要不要容忍这种悬空/暂时找不到目标的 symlink？最好 unix 上默认就放过、Windows 这种本来就不支持 dangling 的平台能给我个明确的报错而不是闷声拷错。顺便希望 junction 在这些 API 里能跟普通 symlink 一样被当作链接处理，别再被当成普通文件或目录处理了。

Expected outcomes:
- `copy_tree` and `install_tree` expose a caller-controlled `allow_broken_symlinks` option for preserving symlinks during tree copies.
- On Unix-like platforms, tree-copy operations preserve broken symlinks by default.
- On platforms where dangling links are not supported, requesting broken-symlink tolerance through `copy_tree` or `install_tree` fails clearly with a symlink-related exception instead of silently copying or misclassifying the entry.
- Links whose targets are also part of the copied source tree are preserved as links in the completed destination tree.
- Junction-style links that Spack treats as links are preserved as link-like entries by `copy_tree`/`install_tree`, rather than being expanded into ordinary directories or files.

Implementation notes:
- The exact data structures, traversal ordering, validation location, and link-detection mechanism are up to the implementation, as long as the public behavior of the tree-copy APIs matches the outcomes above.
- Platform-specific link support may vary, but callers should receive deterministic behavior for the supported `allow_broken_symlinks` modes.
- Keep existing `copy_tree` and `install_tree` behavior unchanged for callers that do not opt into the new option, except where needed to correctly preserve supported link-like entries as links.
