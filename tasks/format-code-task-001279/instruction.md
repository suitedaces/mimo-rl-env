## Session Replay detail page doesn't show backend errors that overlap with the replay

I'm using Session Replay and I have a web app where some backend services throw errors that I track in Sentry. When I open a replay that was recorded during a time window where I know backend errors occurred, the Errors section on the replay detail page is empty — even though I can clearly find those errors in Discover for the same project / same time range.

It seems like the replay page only shows errors when the SDK already associated them with the replay (i.e. when the replay record itself already lists some error ids). If the replay record has no associated errors, the page just shows nothing, and any backend / server-side errors that happened in the same window never surface.

What I'd expect: opening a replay should show me errors from that time window even if the SDK didn't pre-link them. That's the most useful case for me — I open the replay specifically because I want to see what backend stuff blew up while the user was on the page. If the SDK happened to attach error ids to the replay, great, but the page shouldn't depend on that to query for errors at all.

Repro:
1. Trigger a backend error on a route while a Session Replay is being recorded, in a setup where the backend error isn't tied to the replay via the SDK.
2. Wait for the replay to finish and appear in Sentry.
3. Open the replay detail page.

Expected: the backend error shows up in the replay's Errors section.
Actual: the Errors section is empty. The error is visible in Discover for the same project / time range.
