## Problem Statement

I'm using zbpack with a proxy registry configured, and my multi-stage Dockerfiles are breaking — something like `FROM node:20 AS builder` followed by `FROM builder` falls apart because the second `FROM builder` seems to get treated like a real image and gets the proxy prefix slapped on it, so the build can't find the stage anymore. Also looks like the `AS builder` part on the first line gets dropped entirely after rewriting. Can multi-stage builds just work through the proxy rewrite without me having to do anything special?

## Expected outcomes

- Multi-stage Dockerfile `FROM` lines that declare a build stage should keep that stage alias after image reference rewriting. Valid Dockerfile multi-stage `FROM ... AS ...` declarations should continue to work after the rewrite.
- When a proxy registry is configured, a later `FROM` that refers to a previously declared build stage should continue to refer to that stage name as-is, rather than being treated as an external image reference to rewrite.
- Existing single-stage behavior should remain intact: ordinary `FROM <image>` lines without a stage alias should still be rewritten through the configured proxy registry and should remain simple `FROM <image>` lines without an added stage clause or extra trailing content.

## Implementation notes

- The implementation should follow Dockerfile multi-stage build semantics rather than relying on hard-coded stage names or on the specific examples above.
- Implementation details are up to the implementer.
- Non-`FROM` lines and existing proxy rewrite behavior for ordinary image references should not be changed except as needed to support multi-stage builds.
