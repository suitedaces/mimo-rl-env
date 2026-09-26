APM Pod fails to start when using a keystore
When using a keystore the APM Pod fails to start:

```
+ echo 'Initializing keystore.'
+ /usr/share/apm-server/apm-server keystore create --force
Initializing keystore.
Created apm-server keystore
+ for filename in '/mnt/elastic-internal/secure-settings/*'
+ [[ -e /mnt/elastic-internal/secure-settings/logging.verbose ]]
++ basename /mnt/elastic-internal/secure-settings/logging.verbose
+ key=logging.verbose
+ echo 'Adding logging.verbose to the keystore.'
Adding logging.verbose to the keystore.
+ /usr/share/apm-server/apm-server keystore add logging.verbose /mnt/elastic-internal/secure-settings/logging.verbose
could not create secret for: [logging.verbose /mnt/elastic-internal/secure-settings/logging.verbose], you can only provide one key per invocation
```

Seems related to https://github.com/elastic/cloud-on-k8s/pull/1377/files#diff-a45727bb5c0ed9ac8b2a53155dfb83b8L100
