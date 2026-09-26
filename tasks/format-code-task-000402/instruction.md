Amazon SES: support extra_headers, metadata, tags for template sends
Originally, AWS's `ses::SendBulkEmail` API didn't allow specifying email headers. Since Anymail's Amazon SES backend also uses custom headers for `metadata` and `tags`, this meant you [couldn't use](https://anymail.dev/en/stable/esps/amazon_ses/#batch-sending-merge-and-esp-templates) any of the following message options together with a `template_id`:

- `headers` (a.k.a. `extra_headers`)
- `metadata` or `merge_metadata`
- `tags` (except a single tag when using `AMAZON_SES_MESSAGE_TAG_NAME`)

In March, [AWS added a new `ReplacementHeaders` parameter](https://aws.amazon.com/about-aws/whats-new/2024/03/amazon-ses-headers-sending-email/) for `ses::SendBulkEmail`, which allows per-recipient custom headers. In early May, the [new parameter was made available in boto3](https://github.com/boto/boto3/blob/1.34.98/CHANGELOG.rst#L14).

Anymail should use SES's new ReplacementHeaders to support extra_headers, metadata, merge_metadata, and tags in template sends.

(Related: #371)
