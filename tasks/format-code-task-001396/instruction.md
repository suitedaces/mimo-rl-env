## Helm-installed kritis doesn't actually validate pods

I'm trying to set up kritis as a validating admission controller on my cluster, following the helm chart in `kritis-charts/`. After `helm install` I expect any new pod creation to be intercepted by `kritis-validation-hook` and either allowed or rejected based on the ImageSecurityPolicies I've defined. In practice almost nothing about this works end-to-end.

A few problems I hit, roughly in the order I noticed them:

**1. The webhook is never called.** I install the chart, then create a pod with a clearly bad image (not fully qualified, no digest). The pod is admitted immediately. `kubectl get validatingwebhookconfiguration` shows nothing related to kritis — the chart installs the Deployment and Service but never registers anything with the apiserver, so the admission controller is effectively dead code.

**2. The hook pod never becomes Ready.** `kubectl describe pod` on the validation-hook pod shows probe failures against the HTTPS port. The server only serves the admission endpoint, so probing the root path against the TLS port doesn't work and the pod flaps / never goes Ready.

**3. Service / port wiring looks off.** The chart's service is on port 80 with targetPort 443, which doesn't line up with how a webhook is normally reached (apiserver dials the service over TLS on 443). Even if I add a ValidatingWebhookConfiguration by hand, the apiserver can't talk to it through the service as configured.

**4. TLS handshake fails when the apiserver does reach it.** Once I work around the above and point a webhook config at the service, the apiserver complains that the certificate doesn't cover the hostname it's dialing — the in-cluster service DNS names aren't in the cert at all. The CSR template in `kritis-charts/certs.yaml` only sets country/state/locality/org and no subject alternative names, so the generated cert isn't usable for `kritis-validation-hook.<ns>.svc` style addresses that the apiserver uses.

**5. Denials look like webhook failures, not denials.** After I finally get a request through to the handler and the policy says "deny", the apiserver logs it as a webhook *call failure* rather than as a clean rejection of the pod. From the kritis side I can see it's returning an AdmissionResponse with `Allowed: false`, so the policy decision itself is correct — but something about how that response is sent back makes the apiserver treat the whole webhook invocation as broken instead of as a denied admission. The end result is that a pod that should be cleanly rejected by policy instead surfaces as "ImagePolicyWebhook failed" to the user creating the pod, and depending on failurePolicy may even slip through.

**6. Errors are invisible.** Several of the failure paths in `admission.go` (bad request body, JSON marshal error, etc.) just set a status code and return — nothing is logged, so when I was trying to figure out which of the above was actually happening I had to guess. Some logging on those branches would help a lot.

Could the chart ship a working webhook setup out of the box (registration + correct service exposure + a cert that's actually valid for the in-cluster DNS names + a healthy pod), and could the handler return denial decisions in a way the apiserver recognizes as "deny" rather than "webhook broken"?
