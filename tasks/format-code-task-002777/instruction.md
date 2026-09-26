## Timestamp display in Logs Explorer detail panels is inconsistent across log types

When I open a row in the Logs Explorer and look at the side panel, the timestamp field looks completely different depending on which kind of log I'm viewing. A few examples from what I see today:

- **Database API logs** — the panel shows a row labelled "Timestamp" with the raw value (a giant unix microsecond number like `1665432198765000`). Not human readable.
- **Database Postgres logs** — there's no timestamp shown in the detail panel at all. I have to guess from the row in the table.
- **Auth logs** and **Default preview logs** — the row is labelled "ISO Timestamp" and shows an ISO string.
- **Function invocations** and **Function logs** — there *is* a "Timestamp" row, but it's formatted via a one-off `dayjs(log.timestamp / 1000).format('DD MMM, YYYY HH:mm')` per renderer, so the format is yet another variant and doesn't match the Auth/Default panels.

So depending on which log source I'm on, the same conceptual field (when did this happen?) is labelled differently, formatted differently, or missing entirely. It's confusing when jumping between log types and it makes copying the timestamp out useless in some cases (you get a raw unix micro number from the DB API panel).

I'd expect every log detail panel to show the timestamp the same way — same label, same readable formatting — regardless of which renderer is being used, and for the Postgres panel to include it too.
