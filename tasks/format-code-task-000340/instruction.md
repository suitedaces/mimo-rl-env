Error when arkade get helmfile mac m1
<!--- Provide a general summary of the issue in the Title above -->

Arkade fails when trying to install helmfile:

```bash
arkade get helmfile
Downloading: helmfile
2022/09/02 11:34:33 Looking up version for helmfile
2022/09/02 11:34:34 Found: v0.144.0
Downloading: https://github.com/roboll/helmfile/releases/download/v0.144.0/helmfile_darwin_386
Error: incorrect status for downloading tool: 404
```

## Expected Behaviour
<!--- If you're describing a bug, tell us what should happen -->
<!--- If you're suggesting a change/improvement, tell us how it should work -->

arkade successfully installs helmfile

## Current Behaviour
<!--- If describing a bug, tell us what happens instead of the expected behavior -->
<!--- If suggesting a change/improvement, explain the difference from current behavior -->

404 not found

## Are you a GitHub Sponsor yet (Yes/No?)

<!-- Requests from sponsors take priority -->
<!--- Check at https://github.com/sponsors/alexellis -->

- [ ] Yes
- [x] No

## Possible Solution
<!--- Not obligatory, but suggest a fix/reason for the bug, -->
<!--- or ideas how to implement the addition or change -->

1. helmfile migrated to dedicated org, owner field should be updated to `helmfile`
2. in the new repo binary is replaced by archive with `tar.gz`, so we need to update template
3. Condition should be added 
```go
{{- else if or (eq .Arch "aarch64") (eq .Arch "arm64") -}}
{{$arch = "arm64"}}
```

## Steps to Reproduce (for bugs)
<!--- Provide a link to a live example, or an unambiguous set of steps to -->
<!--- reproduce this bug. Include code to reproduce, if relevant -->
1. run `arkade get helmfile`
4.
5.
6.

## Context

<!--- How has this issue affected you? What are you trying to accomplish? -->
<!--- What would happen if this issue was not resolved for you in some way? -->
<!--- Providing context helps us come up with a solution that is most useful in the real world -->

Can't install helmfile via arkade

## Your Environment

* What Kubernetes distribution are you using?

```
Client Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.0", GitCommit:"a866cbe2e5bbaa01cfd5e969aa3e033f3282a8a2", GitTreeState:"clean", BuildDate:"2022-08-23T17:36:43Z", GoVersion:"go1.19", Compiler:"gc", Platform:"darwin/arm64"}
Kustomize Version: v4.5.7
```

* Operating System and version (e.g. Linux, Windows, MacOS):

```
Darwin mariakot-osx 21.6.0 Darwin Kernel Version 21.6.0: Wed Aug 10 14:28:35 PDT 2022; root:xnu-8020.141.5~2/RELEASE_ARM64_T8101 arm64
```

* What arkade version is this?

```
Version: 0.8.39
Git Commit: 2e76c2c3681a3796b03483c3c04fb2ebcba0fa3e
```
