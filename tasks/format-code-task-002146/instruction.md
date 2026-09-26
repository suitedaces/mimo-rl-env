**Describe the bug**
The `@api`  method [`ol/sourec/VectorTile#getFeaturesInExtent`](https://openlayers.org/en/latest/apidoc/module-ol_source_VectorTile-VectorTile.html#getFeaturesInExtent) has been removed, but no mention anywhere.

Assuming it was an accident.

`ol/source/VectorTile getFeaturesInExtent` removed:
https://github.com/openlayers/openlayers/commit/01702e09af859904dac845245b5d5c90fff97e7f#diff-0fbd98d084623d42529972aee3467ed5148d999b1ed748a579dc6a168a5f58aeL174-L218

empty `ol/layer/VectorTile getFeaturesInExtent` added:
https://github.com/openlayers/openlayers/commit/b4cf22f4f2da0ac7ac28976274283422dec09c02#diff-8a7439796df6dff9652e3571b44e43ab1d608fb2495eb00ffdca1dde07ba184cR190-R191
and changed in typescript tests:
https://github.com/openlayers/openlayers/commit/b4cf22f4f2da0ac7ac28976274283422dec09c02#diff-b1298f99049b1adb4683dac2e68abf20d75bcf26d8be53f3e0c98c65c4dfa719L15-R15
These tests pass because this `getFeaturesInExtent` has no type annotations and returns `any` type.

**Expected behavior**
- working typescript tests
- either a breaking changelog or add the method back if it was an accident
- remove or implement `ol/layer/VectorTile getFeaturesInExtent`
