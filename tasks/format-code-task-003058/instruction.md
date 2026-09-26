## Copy/paste leaks objects the user is not allowed to view

We have a Zope site with a folder that mixes content of different sensitivity, e.g.:

```
/projects/
    public_readme        # everyone can View
    internal_notes       # restricted: only certain roles have View
    budget_2017          # restricted: only certain roles have View
```

The View permission on `internal_notes` and `budget_2017` is locked down so that a regular member of the site cannot see them — they don't show up in listings for that user, they can't be traversed directly, etc. So far so good.

The problem appears when that same regular user uses the standard ZMI copy/paste machinery on the **parent** folder `projects`. The user has copy/move and "add Folder" rights in their own workspace, so they:

1. Go to `/projects`, select it, click Copy.
2. Navigate to `/workspaces/alice/`, click Paste.

The paste succeeds, and now `/workspaces/alice/projects/` exists as a copy. But when we inspect it, the copy contains **all three** children, including `internal_notes` and `budget_2017` — the very objects the user was never supposed to see. Because alice owns the new copy in her own workspace, she now has full access to the duplicated `internal_notes` and `budget_2017`, effectively bypassing the permissions that were set on the originals.

This isn't limited to one level either: if a restricted item is nested deeper (say `/projects/team_a/secret_plan`), copying `/projects` still produces a copy that contains the deep restricted item. Any container along the way being copyable seems to drag in everything underneath, regardless of whether the acting user could view those descendants in the original location.

I would expect copy/paste to honor the View permission of the user performing the copy: if the user cannot View a sub-object in the source, that sub-object should not appear in the copy at all. The resulting copy should look, contents-wise, like what the user would have seen if they had listed the source folder themselves — restricted children simply aren't there.

Is this something that can be fixed in `OFS` copy support? Right now it's a real concern for any site that relies on per-object View restrictions inside otherwise-copyable folders.
