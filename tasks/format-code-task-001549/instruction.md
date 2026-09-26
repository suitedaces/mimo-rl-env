## Can't format the timezone name (e.g. `EST`, `Eastern Standard Time`) after `.tz()`

I'm building a meeting/schedule UI with `dayjs` + the `timezone` plugin + the `advancedFormat` plugin, and I'd like to render times together with the human-readable name of the zone, e.g.

```
2020-04-22 09:00 EST
```

or with the long form:

```
2020-04-22 09:00 Eastern Standard Time
```

In moment.js this is what `z` / `zzz` give you in the format string, and since `advancedFormat` is the plugin that fills in moment-compatible tokens, I expected the same to work here:

```js
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import advancedFormat from 'dayjs/plugin/advancedFormat'

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(advancedFormat)

const t = dayjs.utc('2020-04-22 13:00').tz('America/New_York')

console.log(t.format('YYYY-MM-DD HH:mm z'))    // wanted: 2020-04-22 09:00 EST
console.log(t.format('YYYY-MM-DD HH:mm zzz'))  // wanted: 2020-04-22 09:00 Eastern Standard Time
```

What I actually get is the literal token characters left in the output — they don't get replaced at all, so I end up with something like `2020-04-22 09:00 z` / `2020-04-22 09:00 zzz` in my UI.

I also looked through the `timezone` plugin to see if there was some other way to retrieve the zone's display name (so I could append it manually), but I couldn't find anything — once you call `.tz('America/New_York')`, the resulting instance doesn't seem to expose the zone name in any human-readable form, only the numeric offset.

A couple of things that I think matter:

- The output **must** reflect the zone passed to `.tz(...)`, not the machine's local zone. Otherwise users in different regions would see different labels for the same scheduled meeting, which defeats the point of using `timezone` in the first place.
- It should also work with DST — if I take a moment in summer in `America/New_York`, I'd expect `EDT` / `Eastern Daylight Time` instead of `EST` / `Eastern Standard Time`, since that's how the zone actually behaves at that instant.
- Both a short form (`EST`, `PDT`, `CET`, ...) and a long form (`Eastern Standard Time`, ...) would be great to have, the same way moment exposes them.

Could `advancedFormat` (in combination with `timezone`) be extended so that the format string supports rendering the timezone name of the bound zone? Happy to help test if there's a tentative implementation.

It would also be useful to have a direct accessor on the dayjs instance (something like `.offsetName('short')` / `.offsetName('long')`) so the zone label can be obtained programmatically without going through `format`.
