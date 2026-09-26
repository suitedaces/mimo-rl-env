# Support reusable Components in kustomizations

Kustomize today is great at *inheritance*: an overlay layers changes on top of
a base. It is poor at *composition*. If several environments share a chunk of
configuration (an ingress, a stub server, a set of replica overrides, a
configmap tweak), there is no clean way to factor that chunk out and pull it
into more than one environment. Putting the shared piece in its own overlay and
pointing several overlays at it leads to the classic diamond problem: the shared
base ends up accumulated twice and the build fails with duplicate-resource or
"failed to find target for patch" errors.

We want first-class support for reusable **Components**.

## What a Component is

A Component is a directory that contains a kustomization file just like a normal
kustomization, except its `kind` is `Component` (with apiVersion
`kustomize.config.k8s.io/v1alpha1`) instead of `Kustomization`. It may use the
same directives an ordinary kustomization uses — `resources`, `namePrefix`,
`patchesStrategicMerge`, `replicas`, `configMapGenerator`, and so on.

## How Components are referenced

A kustomization gains a new top-level list field, `components`, holding paths to
component directories. For example:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- ../base
- db.yaml
components:
- ../my-component
```

## Required behavior

A component is *inserted into the resource tree as the parent of everything that
has already been accumulated at the point it is reached*. Concretely:

- The `components` of a kustomization are processed **after** its `resources`,
  in the order listed.
- When a component is applied, it operates on the resources accumulated so far
  (the parent's earlier `resources`, plus any earlier components) **together
  with** any resources the component itself declares. Its `namePrefix`,
  generators, transformers, and patches therefore affect that whole combined
  set — a component can patch or rename a resource it never defined, as long as
  that resource was accumulated before the component runs.
- Because each component folds into the same accumulation rather than producing
  an isolated copy of the base, the same base can be reached through several
  components without the diamond duplication problem.
- Multiple components apply in sequence; each sees the effect of the ones before
  it.

## Kind enforcement

The `kind: Component` resource type must be accepted when (and only when) used as
a component:

- A directory whose kustomization is `kind: Component` may **not** be listed
  under `resources`. Attempting to do so must fail the build with an error that
  identifies the `Component` kind.
- A directory whose kustomization is an ordinary `Kustomization` may **not** be
  listed under `components`. Attempting to do so must fail the build with an
  error that identifies the `Component` kind.

The change should be observable through `kustomize build`: a build that composes
components must merge, generate, patch, and prefix resources across the composed
hierarchy and emit the expected resources in a deterministic order.
