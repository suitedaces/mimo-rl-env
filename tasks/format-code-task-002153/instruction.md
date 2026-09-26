## `Image.DockerImageLayers` order is inconsistent across schema versions

I'm writing some tooling on top of the OpenShift image API that needs to walk
image layers in a known order (e.g. to find the base layer, or to compare two
images layer-by-layer). I'm reading `DockerImageLayers` off the `Image` object
that comes back from the API.

The problem is that the order I get back depends on where the image originally
came from:

- For some images, `DockerImageLayers[0]` is the bottom (base) layer and the
  last entry is the topmost layer.
- For other images, it's the other way around — `DockerImageLayers[0]` is the
  topmost layer.

As far as I can tell this correlates with the manifest schema of the image
(`DockerImageManifestMediaType`) — images imported from a v1-style manifest end
up with one ordering, and images imported from a v2-style manifest end up with
another. From a consumer's point of view that's pretty surprising: I just have
an `Image` object in my hand, and I have to special-case on the manifest media
type to figure out which end of the slice is the base.

What I'd like:

1. The layer order exposed on `Image.DockerImageLayers` should be consistent
   regardless of which manifest schema the image was originally pulled from.
   Two images that contain the same layers in the same physical order should
   look the same in the API, no matter where they came from.

2. There should be some explicit, machine-readable signal on the `Image`
   itself that tells a consumer what direction the layers are in, so I don't
   have to infer it from the manifest media type (or guess). Right now I have
   no reliable way to know.

Without (2), even if (1) is fixed today, I have no way to defend my code
against the ordering silently flipping again in the future, and no way to deal
with `Image` objects that were stored before the fix went in.

For (2) I'd expect the signal to live in the standard `Annotations` map on the
`Image`, with something like a `DockerImageLayersOrderAnnotation` key whose
value is one of `DockerImageLayersOrderAscending` / `DockerImageLayersOrderDescending`.
