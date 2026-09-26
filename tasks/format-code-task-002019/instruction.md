## Problem Statement

Hey, something weird is going on with my Saved Projects in earthdata-search. When I open the page I'm seeing projects show up that I definitely didn't create — looks like stuff from another account — and when I try to delete one of them it just errors out. I have a hunch it's because I log into a couple of different EDL environments with the same username, but I'm not sure. Also while I'm in there, the little share link popover on a saved project won't go away when I click somewhere else on the page, I have to click the share button again to close it.

## Expected outcomes

- Saved Projects data should be scoped to the currently authenticated account, even when multiple accounts from different login environments share the same visible username.
- A user should only see their own saved projects in the project-listing response, and deleting one of those visible projects should not fail because another account has the same visible username.
- On the Saved Projects page, an open share-link popover should dismiss when the user clicks outside the popover.
- On the Contact Information page, the form heading should use the page-level heading presentation and display “Contact Information”.
- The “Edit Profile in Earthdata Login” control should visually indicate that it opens an external destination, with the icon presented on the right side of the label.
- The Contact Information form spacing should align with the surrounding page layout rather than adding its own extra inner padding.

## Implementation notes

- The exact data lookup strategy, query structure, component organization, and styling approach are up to the implementer as long as the externally visible behavior matches the outcomes above.
- Keep the Saved Projects ownership behavior consistent across listing and subsequent user actions such as deletion.
- Prefer black-box observable behavior for UI interactions and rendered output; internal helper names, private component structure, and implementation paths do not matter.
