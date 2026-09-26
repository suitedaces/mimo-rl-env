## Precipitation intensity / volumetric flux units aren't auto-converted between metric and US customary

I have a couple of weather-related sensors that report rain rate. Depending on the integration they expose `device_class: precipitation_intensity` (or `speed`) with a unit like `mm/h`, `mm/d`, `in/h` or `in/d` (the `UnitOfVolumetricFlux` units).

When my Home Assistant instance is set to the US Customary system, sensors reporting in `mm/h` keep showing `mm/h` in the UI — they're not converted to the equivalent inches-based unit. Same the other way around: on Metric, an `in/h` sensor stays in `in/h`.

For comparison, plain `precipitation` (cumulative depth in `mm` / `in`) and `speed` sensors using `m/s`, `km/h`, `mph`, `ft/s` do get auto-converted when I switch unit systems — that part works fine. It's only the per-time "flux" variants (`*/h`, `*/d`) that don't get picked up.

Could the unit system handle these the same way? i.e. on Metric, inch-based precipitation intensity / speed should display in mm-based, and on US Customary, mm-based should display in inch-based.
