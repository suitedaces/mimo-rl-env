# Support MySQL, OSS and S3 workspace backends

Today a workspace can only declare a `local` backend for storing state. We want the workspace
configuration to additionally understand three remote backends — a MySQL database (`mysql`), an
Alibaba Cloud OSS bucket (`oss`) and an AWS S3 bucket (`s3`) — and to validate and complete them
correctly.

## Backend configuration schema

Extend the workspace backend configuration so that, in addition to `local`, a user can configure
one of the following backends. The configuration types live in the workspace API package and are
referenced from the existing `BackendConfigs` container (whose existing `Local` field stays as is).
Add a field for each new backend — `Mysql`, `Oss` and `S3` — pointing at a dedicated config type:

- **mysql** (`MysqlConfig`): a database name (`DBName`), a user (`User`), an optional password
  (`Password`), a host (`Host`), and an optional port (`Port`, a `*int`).
- **oss** (`OssConfig`): an endpoint (`Endpoint`), an optional access-key id (`AccessKeyID`), an
  optional access-key secret (`AccessKeySecret`), and a bucket (`Bucket`).
- **s3** (`S3Config`): an endpoint (`Endpoint`), an optional access-key id (`AccessKeyID`), an
  optional access-key secret (`AccessKeySecret`), a bucket (`Bucket`), and an optional region
  (`Region`).

(How you factor the shared object-storage fields of oss/s3 internally is up to you.) Only the
connection-identifying fields are stored in the workspace; the credentials (passwords / access
keys) and the S3 region are sensitive or environment-specific and may instead be supplied through
environment variables (see *Completion* below).

## Validation

Extend the existing backend-configs validation (`ValidateBackendConfigs`) to enforce the following
rules. As before, a `nil` or empty backend configuration is valid (it implies the default `local`
backend), and validation must never inspect values that are only ever provided through the
environment (access keys, mysql password, s3 region).

- **At most one backend** may be configured. Configuring two or more backends at once is invalid.
- **local**: unchanged from current behavior.
- **mysql**: the database name, the user and the host are all required. If a port is given it must
  be in the range 1–65535; an absent port is allowed. The password is never required here.
- **oss**: the bucket and the endpoint are required. The access keys are never required here.
- **s3**: the bucket is required. The endpoint, region and access keys are never required here.

Invalid configurations must produce a non-nil error; valid ones must not.

## Determining the configured backend

Provide a function `GetBackendName` that, given a backend-configs value, reports the name of the
backend that is configured: `"local"`, `"mysql"`, `"oss"` or `"s3"`. When nothing (or only an
empty/`nil` configuration) is set, the reported backend name is `"local"`.

## Completion

Provide a function `CompleteWorkspace` that *completes* a workspace in place — filling in defaults
and overlaying any secrets/region found in the environment onto the configured backend. It must be
safe to call on a workspace with no backend (or the local backend) and must:

- default the mysql **port** to `3306` when it is not set, leaving an explicitly-set port untouched;
- for mysql, set the password from `KUSION_BACKEND_MYSQL_PASSWORD` when that variable is non-empty;
- for oss, set the access-key id from `OSS_ACCESS_KEY_ID` and the access-key secret from
  `OSS_ACCESS_KEY_SECRET` when those variables are non-empty;
- for s3, set the access-key id from `AWS_ACCESS_KEY_ID`, the access-key secret from
  `AWS_SECRET_ACCESS_KEY`, and the region from `AWS_REGION`, falling back to `AWS_DEFAULT_REGION`
  when `AWS_REGION` is empty — each only when the resolved value is non-empty.

A non-empty environment value overrides whatever is already present in the config for that field;
an empty/unset variable leaves the existing value untouched.
