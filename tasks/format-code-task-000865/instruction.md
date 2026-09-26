[logstash] Reload k8s pod if the k8s secrets changed
**Describe the feature:**
Restart k8s pod when secrets changed
Should to add `secretsechecksum` to the statefulset annotation.    

**Describe a specific use case for the feature:**
We updated secrets which mounted to the statefulset, but pod know about the only old secrets, pod should be restarted as in the case of `logstash-config` changed.

I can prepare  the **PR**.
