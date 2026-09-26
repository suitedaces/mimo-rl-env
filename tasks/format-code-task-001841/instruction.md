## `GetLegendGraphic` with `format=application/json` only returns the legend for the first source of a multi-source layer

I have a mapproxy WMS layer that aggregates several upstream WMS layers (think roads + landuse + buildings rolled into one `layer:` entry in my config). When the client UI asks for the combined legend, this works as expected for raster output – the PNG response contains the legend graphics of all the upstream layers stitched together into one image.

The problem is JSON. Our frontend prefers `application/json` legends because it lets us style the legend entries ourselves instead of just dropping a bitmap into the page. When we request the same layer with

```
.../service?REQUEST=GetLegendGraphic&LAYER=mycombined&FORMAT=application/json&...
```

the response only contains the legend information for **one** of the upstream sources (the first one in the configuration). The legend data for all the other sources that make up the layer is missing from the JSON payload.

So PNG gives me the full picture (all source legends combined), but JSON silently drops everything except the first source. From a user point of view both formats are asking for "the legend of this layer", and since the layer is defined as the combination of several sources, the JSON answer should reflect all of them, the same way the PNG one does.

Could mapproxy please produce a combined JSON legend for multi-source layers, so the JSON output is consistent with the PNG output?
