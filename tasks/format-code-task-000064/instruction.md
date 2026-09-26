## Problem Statement

I noticed our Datadog CI Visibility events are showing credentials from URLs, like the token in our Git remote ending up in `git.repository_url`, and even `GITHUB_SERVER_URL` leaking into the GitHub Actions CI tags/env vars. Can dd-trace-js strip the username/password/token parts before reporting those URLs?

## Expected Outcomes

- Git repository URLs reported in CI Visibility metadata, including `git.repository_url`, should not include URL username, password, or token userinfo when the source URL contains credentials.
- CI Visibility URL metadata should remove URL userinfo consistently across supported repository and CI URL sources, not only one provider-specific path.
- GitHub Actions URLs derived from `GITHUB_SERVER_URL`, including `ci.pipeline.url` and `ci.job.url`, should not expose credentials from the server URL.
- The `_dd.ci.env_vars` payload should report `GITHUB_SERVER_URL` without URL userinfo.
- Sanitized URLs should retain the non-sensitive address information needed to identify the repository or CI run.

## Implementation Notes

- Apply the sanitization before CI Visibility URL metadata is reported.
- Keep the implementation free to choose its helper structure, parsing strategy, and validation location.
