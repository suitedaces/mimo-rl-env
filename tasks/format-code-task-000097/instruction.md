Remove standalone / fullscreen requirement
The requirement for apps to have a display property of 'standalone' or 'fullscreen', implemented as a result of #143, is problematic.  Many in the web community object to this being considered a web best practice, notably articulated by Jeremy Keith in his [post](https://adactio.com/journal/10708), though I'm not endorsing all the sentiments he expresses there.

For me the question is whether Lighthouse is a community project designed to judge conformance with universally agreed best practices, or whether it is specifically designed to express the proprietary requirements of Google Chrome in respect to offering an install prompt.  If the latter, then since the heuristics/requirements for installability are not subject to a standard, it's totally valid for Chrome to set whatever requirements it likes - though care should probably be taken to ensure that the intersection of all vendors' installability requirements don't leave developers with insufficient control over their own application design.

However, if Lighthouse is a community tool, then this rule could be seen to be narrowing a recent specification that offers developers a range of options for good reasons.  If options like 'browser' and 'minimal-ui' are bad, why are they in the manifest spec?

If this is deemed justfiable on the grounds that 'native apps don't have a URL bar so PWAs shouldn't either' I would point to zoomability as a similar case - we consider sites that disable zoom to be bad practice, despite pinch-zooming the whole UI not typically being a feature offered by native apps.

This topic came up as part of a discussion of PWAs on a [TAG thread](https://github.com/w3ctag/spec-reviews/issues/123).

cc @marcoscaceres @torgo
