## Feature request: a "Hide version" action for automation rules

We maintain a fairly large project on Read the Docs and we tag releases often. To keep things manageable we already use automation rules to auto-activate and build new versions that match certain patterns — that part has been great.

The problem is the version flyout menu. Some of these versions (older minors, prereleases, internal-ish builds, etc.) we still want to keep built and reachable by URL — there are external links and user bookmarks pointing at them — but we really don't want them cluttering the version dropdown or showing up in the search results.

Today the workflow is:

1. We push a new tag.
2. The automation rule kicks in and activates/builds it.
3. We then go into the project's Versions page and manually tick the **Hidden** checkbox on the version we don't want shown.

Step 3 is the painful bit. With new versions coming in frequently it's a lot of manual clicking, and easy to forget.

Looking at the rule configuration page, the available actions today are only:

- Activate version
- Set version as default

It would be really useful if there were also a **Hide version** action, so we could write a regex rule that says "any new version matching X should land as hidden". The expectation would be that such a version still ends up reachable by its URL (i.e. still effectively built/served — same as today when we activate it and then flip Hidden by hand), it just doesn't appear in the flyout menu or search.

Could this be added as a third action option alongside the existing two?
