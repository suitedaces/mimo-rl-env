Allow to skip unit conversion in ninjotiff writer
## Feature Request

**Is your feature request related to a problem? Please describe.**

We are using infrared `SingleBandCompositor` composites with a crude stretch enhancement to write files with multiple writers, including the ninjotiff writer.  The ninjotiff and ninjogeotiff files are described in °C units (user requirement), whereas the input data are in K.  In this case, the ninjotiff writer converts pixel values from K to °C before enhancing the data:

https://github.com/pytroll/satpy/blob/82112a60f843ad0d3fa32c6d49f224bcb00f28d7/satpy/writers/ninjotiff.py#L118-L122

Other writers do not perform any unit conversion or do so in a different way (see #2021).  The consequence is that data values passed to the crude stretch enhancement for ninjotiff production are offset by 273.15 compared to those passed for production with other writers.  For example, if the geotiff or ninjogeotiff writer get

```yaml
kwargs: {stretch: crude, min_stretch: 313.5, max_stretch: 186}
```

then producing the same images with the ninjotiff writer would need

```yaml
kwargs: {stretch: crude, min_stretch: 40, max_stretch: -87}
```

which is a problem.

The good news is that unit conversion isn't actually needed with the ninjotiff writer.  So far, we accidentally didn't use any, by using a `GenericCompositor` rather than a `SingleBandCompositor`, which means our units attribute was lost and conversion did not occur.  Instead, we pass `ch_min_measurement_unit` and `ch_max_measurement_unit` (in °C), which the ninjotiff writer uses to calculate the scale (slope) and offset (axisintercept), independently of what's happening in the crude stretch (it's up to the user to ensure consistency).  By skipping unit conversion altogether and setting temperature limits both in the enhancement definition and in the writer parameters, we get images that look as intended and have the correct values in °C encoded.  This is not ideal either, but corresponds to the status quo.

**Describe the solution you'd like**

I would like that the ninjotiff writer gets a way to skip unit conversion.  For example, a parameter `convert_temperature_units`, which defaults to True.  If set to False, no unit conversion is performed, and the same crude stretch enhancement parameters can be used when producing ninjotiff or other formats.

**Describe any changes to existing user workflow**

None.  The status quo would remain the default behaviour.

**Additional context**

Other solutions could be:

- Define special composites for ninjotiff production, with their own enhancements, where parameters are defined in °C rather than K.  This would work, but it would require duplicating all IR composites and enhancements and make trollflow2 production more complicated.  Products would be defined in two different places, which is not ideal for maintenance purposes.
- Change the behaviour of the ninjogeotiff writer to be similar to the ninjotiff writer (see #2021).  This would mean that the same enhancement configuration (in °C) can be used for both writers.  This is not ideal, because other writers (such as regular geotiff) would still need different parameters.
- Produce images in units of K and leave it to the client to convert units if users wish to display other units.  In this case the client would be NinJo.  There are good arguments for this approach and this might even be implemented eventually, but is not under my control and I need a solution sooner than such an implementation can be expected.
- Something else I'm not thinking of.

See also #2018 and #2021.
