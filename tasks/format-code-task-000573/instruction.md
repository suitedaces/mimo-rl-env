## LiveTable silently drops fields it can't display

I'm using `LiveTable` with a list of fields I want to watch during a scan. Some of those fields end up not showing up in the printed table at all — no column header, no values, nothing. The scan otherwise runs fine.

After poking around for a while I figured out it's happening for fields whose `dtype` in the descriptor isn't one of the simple scalar types LiveTable knows how to format (e.g. array-valued detector channels). That's fair enough — LiveTable obviously can't print an arbitrary array as a single table cell — but the fact that it just disappears with zero feedback is really confusing. The first time it happened I thought I'd typo'd the field name, or that my detector wasn't producing data, and spent a while chasing the wrong thing.

It would be much nicer if LiveTable told me when it's dropping a requested field because it doesn't know how to render its dtype, so I at least know to either remove that field from my list or send it to a different callback.
