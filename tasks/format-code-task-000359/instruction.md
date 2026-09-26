I'm running `ensure-sca-scanner` on a repo that uses JFrog Pipelines, and Rule 10 is still reporting that there's no SCA scanner configured. The pipeline has a step that runs `jf xr ...`, so I'm not sure if allero is missing the JFrog pipeline config or just not recognizing the Xray CLI command.

Expected outcomes:
- Rule 10 / `ensure-sca-scanner` treats SCA scanner configuration found in JFrog Pipelines as satisfying the scanner requirement.
- A repository that only configures its SCA scan through JFrog Pipelines should not be reported as missing an SCA scanner.
- Commands using the JFrog Xray CLI form `jf xr ...` should be recognized as SCA scanner invocations when they appear in supported CI/CD pipeline command steps.
- Existing SCA scanner detection in GitHub Actions and GitLab CI should continue to work.

Implementation notes:
- The exact parsing approach, data structures, and helper organization are up to the implementer.
- Keep the behavior focused on Rule 10’s externally observable pass/fail result rather than on any particular internal representation.
