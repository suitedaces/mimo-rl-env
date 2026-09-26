Default to Anonymous Access when no identity config is present
Currently the AuthConfig requires at least one identity evaluator config to be present or all requests will fail with `401 Unauthorized`. One who wants to skip identity verification phase needs to explicitly add a trivial `anonymous: {}` identity config.

This is an RFE to make this the standard behaviour when no identity evaluator config is present in the AuthConfig.
