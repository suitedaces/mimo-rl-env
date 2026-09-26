## Maintenance windows should run weekly, not monthly

We've been running Fleet with the Google Calendar integration enabled and a few calendar policies configured so that hosts which fail compliance checks get a scheduled maintenance window on the end user's calendar.

The current cadence is too slow for how we want to operate. As far as I can tell from watching events land on people's calendars, a host that starts failing a calendar policy only gets a maintenance window scheduled roughly once a month — and if the relevant day in the current month has already passed by the time the host starts failing, the event jumps all the way to next month. That means an end user can be sitting on a non-compliant device for several weeks before the next window comes around, which defeats the point of having the automated nudge.

We'd like the maintenance window to be scheduled on a weekly cadence instead. The "always lands on a Tuesday" part is actually nice — it gives end users a predictable mid-week day to expect interruptions on, and we'd like to keep that. But it should be *every* Tuesday going forward from when the host starts failing, not one specific Tuesday per month.

Concretely, the behavior we want:

- Host starts failing a calendar policy today → the maintenance window is placed on the next upcoming Tuesday (which could be today, if today is Tuesday).
- It should not skip ahead by weeks just because some "preferred" Tuesday in the month is already behind us.

Could the scheduling logic for these calendar events be switched over to a weekly Tuesday cadence?
