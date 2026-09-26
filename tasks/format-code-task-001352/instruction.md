### Consolidate the `buildpacks` package into a single `Client`

Looking at `pkg/kf/buildpacks/`, we currently expose three separate interfaces, each with its own constructor, its own implementation file, and its own generated fake:

- `BuilderCreator` (in `builder_creator.go`) — `Create(dir, containerRegistry)`
- `BuildTemplateUploader` (in `build_template_uploader.go`) — `UploadBuildTemplate(imageName)`
- `BuildpackLister` (in `buildpack_lister.go`) — `List()`

Every command under `pkg/kf/commands/buildpacks/` that wants to do anything buildpack-related has to take one or two of these as separate dependencies. For example `NewUploadBuildpacks` currently takes both a `BuilderCreator` and a `BuildTemplateUploader`, and the wire injector in `wire_injector.go` has to wire up the constructors independently.

This is inconsistent with how the rest of the codebase organises its packages. `apps`, `services`, `servicebindings`, and `spaces` all expose a single `Client` interface that groups the related operations together, with a single `NewClient` constructor and a single generated fake. The buildpacks package is the odd one out.

It would be nice to refactor `pkg/kf/buildpacks` to follow the same pattern as the other packages — a single `Client` that covers builder creation, build template upload, and buildpack listing — and update the commands and wire setup accordingly. The fake package should collapse to a single fake as well.

No behavioral change is intended; this is purely a structural cleanup to make the buildpacks package consistent with the rest of the repo.
