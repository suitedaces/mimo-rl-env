## Stale call forwarding icon on DSDS device when one SIM is missing / not ready

I'm using a dual-SIM Firefox OS device. Steps to reproduce:

1. Insert two SIMs (SIM1 + SIM2).
2. Enable call forwarding on SIM1 from the Settings app — the call forwarding indicator for SIM1 shows up in the status bar as expected.
3. Power off, remove SIM1, leave only SIM2 inserted, power on again.

Expected: only SIM2's status is reflected in the status bar. The SIM1 slot has no card, so it should not show a "call forwarding enabled" indicator for that slot.

Actual: the call forwarding icon for the now-empty SIM1 slot is still shown as enabled, as if a card were still there with CF turned on.

I can also reproduce a similar effect by booting with one of the slots holding a card that hasn't fully initialized yet (no iccId available) — the indicator for that slot can show a stale state from a previous session instead of being cleared.

Basically, whenever a slot has no usable SIM (no card, card not ready, or no iccId), its call forwarding indicator should reflect "off" rather than carrying over whatever was last shown for that slot. Right now on DSDS that doesn't happen reliably and the status bar ends up lying to the user about which line has CF enabled.
