## Support dependencies between rich-text features

Third-party rich-text extensions often build on another feature: for example, a custom inline treatment may rely on an existing converter rule and editor control. Today each field has to repeat those prerequisite feature names manually, and an omitted prerequisite can make the editor and stored HTML disagree. Add dependency composition to the public rich-text feature registry so extensions can declare that relationship once and every consumer sees the same effective feature list.

Expose `FeatureRegistry.register_feature_dependency(feature_name, dependencies)`. `dependencies` may be one feature-name string or an iterable of feature-name strings. Multiple declarations for the same feature are additive: preserve first-declaration order and ignore dependency names already declared for that feature.

Expose `FeatureRegistry.resolve_features(features=None)`. Resolve requested features from left to right. For each feature, recursively resolve its dependencies in declaration order and place them before the dependent; emit every feature name at most once. This is a stable dependency expansion, not an alphabetical sort. A dependency name does not need its own dependency declaration, editor plugin, or converter rule: keep such names in the effective list and let each existing consumer apply its normal unknown-feature behavior. Do not mutate the caller's list, and return a fresh list on every call.

Passing `None` to `resolve_features` means resolve the registry's current `default_features`; passing an explicit empty list must remain empty. `get_default_features()` must return the same fully resolved, fresh-list result. Circular dependencies must raise `django.core.exceptions.ImproperlyConfigured` when detected. The message must begin `Cyclic rich text feature dependency: ` and contain the complete cycle as an arrow-separated chain with the starting feature repeated at the end; the starting point within the cycle is not significant.

Use the effective list consistently in the rich-text consumers:

- Draftail must resolve both explicit and default feature lists before constructing plugins. Its `features` value must be the effective ordered list, prerequisite plugins must be constructed first, and an unknown feature must retain the existing `RuntimeWarning` behavior once per distinct effective feature.
- The editor-HTML converter must activate converter rules from dependencies for explicit and default feature lists, without activating unrelated feature rules.
- The content-state converter must do the same for both database-to-content-state and content-state-to-database conversion, including when defaults are used. Its `features` value must reflect the effective list when an explicit list is supplied.

Existing editor-plugin registration and lookup for dependency-free features must remain compatible, including returning `None` for a missing editor or feature.
