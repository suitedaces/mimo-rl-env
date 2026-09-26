## CVE severity card totals don't add up to the table total

When viewing the vulnerabilities page, the total CVE count shown in the table sometimes doesn't match the sum of the per‑severity cards (Critical / Important / Moderate / Low) above it. The mismatch is small but reproducible on clusters that have CVEs whose severity is reported as unknown by the scanner — those CVEs show up in the table row count but aren't reflected in any of the severity cards, so the cards under‑report.

This is confusing for anyone trying to reconcile the numbers ("why does the table say 137 but the cards add up to 134?").

The GraphQL types backing these cards (`ResourceCountByCVESeverity` / `ResourceCountByFixability`) currently only expose buckets for the four named severities, so the frontend has no way to render or include the leftover CVEs even if it wanted to. The backend needs to start surfacing counts for CVEs that fall outside Critical/Important/Moderate/Low (both total and fixable), so the UI can account for every CVE that the table is showing and the cards stop disagreeing with the table.

This applies to the same severity-count plumbing used by both image CVE and node CVE views.
