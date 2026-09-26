### Apache Airflow version

2.10.5

### If "Other Airflow 2 version" selected, which one?

_No response_

### What happened?

When configuring Vault as secrets backend with AWS IAM authentication, for example, when installing Airflow on AWS EKS, and using the IRSA (IAM Role for Service Accounts) of the Airflow Pods to authenticate to Vault, the STS authentication call will fail if Vault is configured with a STS region other than `us-east-1`. This is a pretty common scenario whenever one is not using that region and wants to minimize the latency of STS API calls.
The `region` parameter is never passed to `hvac.api.auth_methods.Aws.iam_login()` by the `airflow.providers.hashicorp._internal_client.vault_client._VaultClient._auth_aws_iam()` method, which [defaults to `us-east-1`](https://github.com/hvac/hvac/blob/ea3a6520cc08f69470494cce0ac26a2ab025f91d/hvac/api/auth_methods/aws.py#L747). 

Example error message:
```
hvac.exceptions.InvalidRequest: error making upstream request: received error code 403 from STS: <ErrorResponse xmlns="https://sts.amazonaws.com/doc/2011-06-15/">
  <Error>
    <Type>Sender</Type>
    <Code>SignatureDoesNotMatch</Code>
    <Message>Credential should be scoped to a valid region. </Message>
  </Error>
  <RequestId>84b47cd7-fc7b-442f-b75b-309b93d2b2ee</RequestId>
</ErrorResponse>
, on post http://vault-active.vault.svc.cluster.local:8200/v1/auth/aws/login
```

### What you think should happen instead?

The AWS region should be configurable as an input parameter of VaultBackend (and _VaultClient), and should default to the boto3 configuration if not provided (from env vars, instance metadata, etc.).

### How to reproduce

Just configure Vault with a regional STS endpoint different than `us-east-1`.

### Operating System

Debian 12 Bookworm

### Versions of Apache Airflow Providers

`apache-airflow-providers-hashicorp==4.0.0`

### Deployment

Official Apache Airflow Helm Chart

### Deployment details

_No response_

### Anything else?

_No response_

### Are you willing to submit PR?

- [x] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
