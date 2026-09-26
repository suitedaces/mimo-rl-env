我给 dynamic preferences 的 Section 配了 verbose_name（比如 General settings），但在 Django admin 的偏好列表、右侧 section 过滤器和编辑页里看到的还是 general，Python 里 str(section) 打出来也是 general。我一开始还以为是 verbose_name 没生效，或者我配置写错了。

Expected outcomes:
- `Section.__str__()` should use a configured human-readable section name when one is provided.
- Sections without a configured human-readable name should continue to display their original section name, and an empty section should still stringify to an empty string.
- In the Django admin preference changelist, each preference’s section display should prefer the human-readable section name and fall back to the original section name when the section cannot be resolved.
- In the Django admin section filter, filter option labels should prefer the human-readable section name and fall back to the original section name when the section cannot be resolved.
- In the Django admin preference edit page, the read-only section display should prefer the human-readable section name and fall back to the original section name when the section cannot be resolved.

Implementation notes:
- Keep existing preference registration, lookup, filtering, and editing behavior intact; this change is only about the externally visible section label shown to users.
- The exact data flow, helper structure, and admin customization approach are up to the implementation, as long as the observable API and admin behavior above are satisfied.
