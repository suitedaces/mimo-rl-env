## Problem Statement

Hey, I've been browsing collections on Earthdata Search and noticed the imagery for some layers looks off — MOPITT CO and a couple of the MISR / CERES EBAF ones are showing up but the tiles don't match what I see for the same products over on Worldview. Worldview renders them fine, so I figured those should just work in Earthdata Search too, but something on your side seems to be overriding it. Could you take a look? Ideally I'd just want what Worldview supports to be what shows up here, without anything extra getting in the way.

## Expected outcomes

- GIBS layer support in Earthdata Search should match the layers and collection associations provided by the upstream Worldview/GIBS product response.
- Collections should only be tagged as GIBS-supported when the upstream Worldview/GIBS data includes matching supported layers for those collections.
- Collections not represented by upstream-supported layers should not be treated as GIBS-supported in generated tags.
- Generated GIBS tags should add and retain only the collection concept IDs derived from upstream-supported layers, while removing the tag from collections outside that derived set.

## Implementation notes

The exact data flow, data structures, and validation location are up to the implementer. Preserve the existing supported-layer filtering rules, but make the final Earthdata Search support/tag output follow the current upstream Worldview/GIBS product data.
