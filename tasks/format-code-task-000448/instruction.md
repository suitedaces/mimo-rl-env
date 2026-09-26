argocd-tls-certs-cm is overwritten on any change as of v0.2.0
**Describe the bug**
Prior to v0.2.0, certificates for TLS validation could be managed via the ArgoCD GUI or by controlling the argocd-tls-certs-cm ConfigMap directly. The value of argocd-tls-certs-cm was set initially when ArgoCD was deployed but not altered thereafter.

After upgrading tov0.2.0, this ConfigMap is reset to the value of tls.intitialCerts in the ArgoCD CR after any change. This renders the certificate management via the GUI or previous direct ConfigMap control useless and deletes any certificates that were added to the ConfigMap prior to the upgrade.

Workaround:  Add the needed cert to ArgoCD CR spec  tls.initialCerts.  
See https://argocd-operator.readthedocs.io/en/latest/reference/argocd/#tls-options.

Workaround example: https://github.com/iam-veeramalla/openshift-gitops-examples/blob/master/argocd/GITOPS-1725/argocd-initialTLScerts.yaml

**Expected behavior**
Revert back to the original behavior

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.
