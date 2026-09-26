## notify-send notifications pile up in the Gnome 3 notification tray

I'm using Guard with the `:notifysend` notifier on a Linux box running Gnome 3. Every time a guard plugin fires (test run finishes, etc.) Guard pops up a notification via `notify-send`, which is what I want — but on Gnome 3 those notifications never go away. They show up briefly on screen and then get parked in the notification bar / message tray, where they accumulate over a session until I manually clear them.

After a few hours of editing I end up with dozens of stale "specs passed" / "specs failed" entries sitting there. On other desktop environments (and on older Gnome) the same notifications just disappear after the timeout, which is the behaviour I'd expect here too — these are transient status pings, not things I want to come back to later.

It looks like this is a known Gnome 3 behaviour for `notify-send`: unless the sender explicitly marks the notification as transient, Gnome 3 treats it as something worth keeping around in the tray (see e.g. https://bugzilla.redhat.com/show_bug.cgi?id=693207#c3). Since Guard's notifications are inherently ephemeral, it'd be nice if the notifysend notifier defaulted to behaviour that lets them auto-dismiss on Gnome 3, instead of every Guard user having to figure this out and configure it themselves.
