# Add a reference indexer for Ingress-referenced Services and Secrets

To make the ingress controller react to changes in resources that an Ingress (or a
Service) depends on, we want to be able to build field-index values that map an
Ingress/Service to the names of the objects it references. Later this will feed
controller-runtime field indexers and event handlers, but for now we just need the
indexing logic itself, living in the ingress package (`pkg/ingress`).

Please add a reference indexer with the following public surface:

```go
// constructs the default reference indexer, reusing the existing builders.
func NewDefaultReferenceIndexer(enhancedBackendBuilder EnhancedBackendBuilder,
    authConfigBuilder AuthConfigBuilder, logger logr.Logger) *defaultReferenceIndexer

func (i *defaultReferenceIndexer) BuildServiceRefIndexes(ctx context.Context, ing *networking.Ingress) []string
func (i *defaultReferenceIndexer) BuildSecretRefIndexes(ctx context.Context, ingOrSvc metav1.Object) []string
```

(`networking` is `k8s.io/api/networking/v1beta1`; `metav1` is
`k8s.io/apimachinery/pkg/apis/meta/v1`.)

## BuildServiceRefIndexes

Given an Ingress, return the names of all Kubernetes Services this Ingress routes
traffic to as backends. Consider both the Ingress's default backend (`spec.backend`,
if present) and every backend referenced from the HTTP paths of `spec.rules`. Rules
without an HTTP section contribute nothing.

A backend can describe its destination directly (a Service name + port) or, when its
port is the magic string `use-annotation`, indirectly through a matching
`alb.ingress.kubernetes.io/actions.<name>` annotation. In both cases the destination is
ultimately a *forward* action whose target groups each point either at a Service (by
name) or at an existing target group ARN. Collect the Service names from those forward
target groups; target groups that reference an ARN rather than a Service contribute no
name.

The result must be deduplicated and sorted in ascending order. If building the backend
for any path fails, the index for that Ingress cannot be trusted — return no names at
all rather than a partial list.

## BuildSecretRefIndexes

Given an Ingress *or* a Service, return the names of the Kubernetes Secrets it
references through OIDC authentication configuration. The OIDC configuration is supplied
via the `alb.ingress.kubernetes.io/auth-idp-oidc` annotation, whose `secretName` field
names the Secret. When that annotation is present, the returned list contains that
secret name; this must hold regardless of whether an `auth-type` annotation is also set
on the object (the same auth annotations may be configured on either an Ingress or a
Service, and a Service can carry the OIDC config on its own).

Objects that reference no OIDC secret — including objects with no auth annotations, or
with only Cognito auth configured — yield no secret names. If the auth configuration
cannot be parsed, return no names.
