# Problem Statement

I'm finding the overlay imports in chaco a bit scattered to work with. I'm pulling in things like PlotLabel, Legend, DataLabel, LassoOverlay, ContainerOverlay, and various inspector/status overlays, and they're each coming from their own top-level module — would be nice if there were a single consolidated place to grab all the overlay and layer stuff from. Could you gather these under one `chaco.overlays` package with its own api module, and have `chaco.api` re-export them too? Ideally the formatter helpers like basic_formatter and the datetime/date/time ones would be reachable from there as well.

# Expected outcomes

- `chaco.overlays.api` should be importable as a public aggregation module for Chaco's existing public overlay, inspector, layer/status, and related formatter symbols that are currently scattered across separate modules.
- Representative overlay/layer symbols such as `PlotLabel`, `Legend`, `DataLabel`, `LassoOverlay`, `ContainerOverlay`, and the inspector/status-related overlays should be reachable from `chaco.overlays.api`.
- The same consolidated public symbols should also be reachable from `chaco.api`, and imports through `chaco.api` should behave as re-exports of the consolidated overlay API rather than unrelated stand-ins.
- The relevant formatter helpers, including `basic_formatter` and the date/time-oriented helpers, should be importable from both `chaco.overlays.api` and `chaco.api`.
- Layer-related package resources should remain available in installed/source distributions after the overlay/layer consolidation, so code using the consolidated overlay/layer package does not lose its required data assets.

# Implementation notes

The concrete organization of files inside the overlay package is up to the implementer, provided the public import behavior above is satisfied. Compatibility handling for older import paths may be implemented as appropriate, but the consolidated `chaco.overlays.api` and `chaco.api` surfaces should be the supported public access points for the consolidated overlay/layer symbols.
