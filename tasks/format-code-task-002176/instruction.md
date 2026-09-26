Expand the Pinned-Dependencies check so a GitHub workflow is evaluated for every externally fetched executable dependency, not just step-level actions. Reusable workflows and container images can execute just as much third-party code as an action, and local actions should not be penalized for lacking a remote revision.

Apply these rules to workflow files under .github/workflows:

- A remote step `uses` action is pinned only when its ref after `@` is exactly 40 hexadecimal characters. Hex digits are case-insensitive. Tags, branches, shorter or longer hashes, missing refs, and dynamic expressions are mutable and must be reported, even when an expression is followed by text that resembles a full SHA.
- A `uses` value beginning with `./` is repository-local and must not produce an unpinned warning. This exemption applies to both step actions and local reusable workflows.
- A job-level `jobs.<job>.uses` that calls a remote reusable workflow follows the same exact-40-hex rule as a remote action.
- A step `uses: docker://...` is a container dependency rather than a Git action ref. It is pinned only by an `@sha256:` digest containing exactly 64 hexadecimal characters; tags, other digest algorithms, and wrong-length digests are mutable.
- Inspect job containers in both supported forms, `container: <image>` and `container: { image: <image>, ... }`, plus every `jobs.<job>.services.<service>.image`. These images use the same exact SHA-256 digest rule as `docker://` actions.

Emit exactly one warning detail for each mutable declaration and none for compliant or local declarations. Each such detail must carry the workflow path in `LogMessage.Path`, identify it as `FileTypeSource`, and include the dependency value exactly as declared so JSON/SARIF consumers can identify the finding. A workflow whose dependencies are all immutable or local must retain the maximum Pinned-Dependencies score with no warnings; any mutable declaration must lower that score without becoming a runtime error.

Do not silently treat a sequence-valued job `container` declaration as safe. It is invalid workflow dependency input, so the check must return its existing runtime-error/inconclusive result. Preserve the existing pinned and unpinned behavior for ordinary step-level remote actions while adding these forms.
