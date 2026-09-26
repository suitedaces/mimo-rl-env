ENH date_range yearly frequency flag 'A' is confusing, 'Y' should be accepted
to get a yearly frequency from date range the flag is actually `freq="A"` (for "Annual" i guess) rather than `freq="Y"` for yearly.

It would seem more consistent if it accepted "Y" as well/instead of "A", following the pattern:

hour -> hourly -> H
day -> daily -> D
week -> weekly -> W
year -> yearly -> Y
