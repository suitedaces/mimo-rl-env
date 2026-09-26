# Problem Statement

When I use CanICA or DictLearning, I always end up doing `masker_.inverse_transform(components_)` just to get something I can plot or save as a Nifti image. Could nilearn expose the learned components directly as an image after fitting, so I don’t have to do that manual unmasking every time?

# Expected outcomes

- Learned component images:
  - After fitting `nilearn.decomposition.CanICA`, the estimator exposes `components_img_` as a 4D Nifti image representing the learned components in image space.
  - After fitting `nilearn.decomposition.DictLearning`, the estimator exposes `components_img_` as a 4D Nifti image representing the learned components in image space.
  - The image available through `components_img_` should be directly usable by normal Nifti-image consumers, such as plotting utilities or saving through the image object’s file-writing API.
  - The image content and shape should correspond to the components that users previously obtained by manually unmasking `components_`.

- Compatibility and user-facing guidance:
  - Existing workflows that access `components_` after fitting should continue to work.
  - User-facing documentation for `CanICA` and `DictLearning` should direct users toward `components_img_` as the preferred image-space representation of learned components.
  - User-facing documentation should make clear that `components_` is the older masked-array representation and that older-version workflows can obtain an image by manually unmasking it.

- Standard estimator convenience:
  - Decomposition estimators derived from `nilearn.decomposition.BaseDecomposition` should provide the standard `fit_transform` convenience API.
  - Calling `fit_transform` should be equivalent to fitting the estimator and then transforming the same input data.

# Implementation notes

- The concrete implementation strategy, storage details, and exact point in the fitting pipeline where image-space components are produced are left to the implementer.
- Preserve the existing public behavior of fitted estimators unless it conflicts with exposing the new image-space component attribute.
- Documentation updates should describe the user-visible behavior without requiring users to depend on private implementation details.
