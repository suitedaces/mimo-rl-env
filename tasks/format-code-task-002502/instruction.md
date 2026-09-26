/kind user-story

## User Story
As an odo developer, I want to know what Devfile stacks are being downloaded by odo and plugins that are using odo So that I can compare usage between plugins and odo cli and better plan new features.

## Acceptance Criteria 
- [ ] if `TELEMETRY_CALLER` (https://github.com/redhat-developer/odo/issues/6147) is set, odo should pass caller information to PullStackFromRegistry function. If odo called from cli callers should be `odo` (as it is now), if `TELEMETRY_CALLER` is set then the caller passed down to PUllStackFromRegistry should be `odo-<TELEMETRY_CALLER>`.







/kind user-story
