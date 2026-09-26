## Reviewer suggestions exclude me and the private repo owner

Two related problems I ran into when trying to add reviewers to a pull request:

**1. I can't request myself as a reviewer**

Someone else opened a PR in a repo where I have write access. I wanted to add myself as one of the reviewers — partly so the PR shows up correctly on my review dashboard, partly so the relevant notifications go out — but I'm not present in the reviewer dropdown at all. I'm not the PR author either, so there's no reason I shouldn't be selectable.

**2. Owner of a private personal repo doesn't show up in the suggestions**

Separately, I have a private repo under my personal user account (not an organization). A collaborator on that repo opened a PR and tried to request me — the repo owner — as a reviewer. My user doesn't appear in the suggestions list at all, so they can't pick me.

(For comparison: if the same setup is an organization-owned private repo, the org members do show up like you'd expect. The "missing" case is specifically when the repo lives under an individual user's account.)

In both cases I'd expect to be selectable. Anyone with read+ access to the repo — including the owner of a private personal-account repo — should be a valid reviewer choice, with the obvious exception of the PR author themselves.
