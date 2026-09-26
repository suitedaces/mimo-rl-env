## Feature request: KMS encryption filter and action for SNS topics

SNS now supports server-side encryption with KMS, and I'd like to manage it with Cloud Custodian, but the SNS resource doesn't seem to expose anything for it.

My use cases:

1. **Audit which SNS topics are encrypted and with which key.** I want to write a policy that selects SNS topics whose KMS master key is (or isn't) one of our approved CMKs — same kind of filtering that other resources support against a KMS key (matching by id / arn / alias). Right now I can only get at it by writing a raw `value` filter against `KmsMasterKeyId`, which doesn't help me match against alias names or filter through KMS key attributes.

2. **Remediate unencrypted topics.** Once I've found topics that aren't encrypted (or are encrypted with the wrong key), I want an action that flips encryption on for them, ideally letting me pick the KMS key. I'd also like to be able to turn encryption back off on a topic if needed.

A rough example of the kind of policy I'd like to be able to write:

```yaml
policies:
  - name: sns-encrypt-with-approved-cmk
    resource: sns
    filters:
      - <something that matches topics not encrypted with our CMK>
    actions:
      - <something that enables SNS encryption with our CMK>
```

Would it be possible to add KMS-aware filtering and an encryption-management action to the `sns` resource?
