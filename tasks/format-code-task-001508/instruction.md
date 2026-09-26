## PrusaLink: expose more printer telemetry as sensors

The PrusaLink integration currently exposes only a handful of values from the printer (state, current heatbed temperature, current nozzle temperature, and the job-related sensors). When I'm watching a print from Home Assistant, that's not really enough to know what's going on.

Things I'd like to be able to see as sensors but currently can't:

- **Target temperatures** for the heatbed and the nozzle. Right now I can only see the current temperatures, so I can't tell from HA whether the printer is heating up to a setpoint, holding it, or cooling down.
- **Z-height** of the print head — useful to know roughly how far into a print we are, especially for tall prints.
- **Print speed** (the live speed % the printer is running at, which can be changed on the printer's screen during a print).
- **Material** currently configured / loaded on the printer.

All of this is already available from the PrusaLink API response that the integration polls — it just isn't surfaced as entities in Home Assistant. Could these be added to the sensor platform so I can use them in the dashboard and automations?
