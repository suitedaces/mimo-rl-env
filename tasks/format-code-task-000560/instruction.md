## `charging_start_time` shows wrong time for scheduled charging

I'm using `bimmer_connected` from my Home Assistant setup to surface the planned charging start time of my BMW on a dashboard. The car has a charging window configured (e.g. starts at 23:00 local time) and is plugged in but not yet charging — so the state is `WAITING_FOR_CHARGING`.

What I see on `fuel_and_battery.charging_start_time` does not match what the official MyBMW app shows:

- In the app the planned start is, say, **today 23:00** (my local time).
- In `bimmer_connected` I get a datetime that is several hours off from what the app shows. I'm not in UTC, and the offset matches my timezone difference, so the hour/minute coming from the API is being interpreted as if it were UTC.
- Even worse, if I poll after the window's start hour has already passed (e.g. I check at 00:30, just after midnight), I still get a `charging_start_time` that lies in the past for today, instead of rolling over to tomorrow's window. A "planned" start time pointing into the past is obviously not useful — Home Assistant happily displays "-2 hours" relative to now.

Minimal repro of how I use it:

```python
# in WAITING_FOR_CHARGING state
print(vehicle.fuel_and_battery.charging_start_time)
# e.g. window is 23:00 local, current local time is 00:30 the next day
# -> got a datetime for 'yesterday 23:00 UTC' (or similar)
# -> expected: tomorrow's window start, in local time, matching the BMW app
```

Expected:
- `charging_start_time` should match what the BMW app shows the user (i.e. the local-time hour/minute coming from the charging window).
- It should always refer to the **next** occurrence of that hour/minute — if today's window is already in the past, it should be tomorrow.

---

While I'm at it, a smaller related observation: `climate.activity_end_time` seems to be computed relative to "right now" at parse time rather than the time the data was actually fetched from the server. If I look at the same fetched payload a few seconds later (or replay it), the end time drifts. It would be nicer if it were anchored to the fetch timestamp so the value is stable for a given response.
