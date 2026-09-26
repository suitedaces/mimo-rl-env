**Bug: "Estimated years attending" dropdown doesn't update the view**

In the Paying for College disclosures tool, changing the "Estimated years attending" dropdown does nothing — the rest of the disclosure view doesn't react to the new selection. The sections of the page that should reflect a different program length stay exactly as they were.

If I open the browser dev tools and watch the console while changing the dropdown, an error is logged each time. So it looks like the change handler is blowing up rather than just silently doing nothing.

**Steps to reproduce**
1. Open the Paying for College disclosures tool.
2. Open the browser developer console.
3. Change the "Estimated years attending" dropdown to a different value.

**Expected**
The view re-renders to reflect the newly selected program length.

**Actual**
Nothing visible changes, and an error shows up in the console.
