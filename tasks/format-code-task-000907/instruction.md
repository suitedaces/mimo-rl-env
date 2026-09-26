Subscriptions are not copied when duplicating a project

When I use the "Duplicate current project" option in the project settings UI to clone an existing project, all of the project variables and aliases get carried over to the new project, but none of the notification subscriptions on the source project show up under the new project. I have to recreate every subscription by hand.

Same thing happens via the REST API `POST /rest/v2/projects/{project_id}/copy` — vars and aliases come through, subscriptions don't.

For our team, the subscriptions (build/task failure notifications, etc.) are a big part of what makes the source project's setup useful, so having to redo them every time we fork a project is painful. Copying a project should copy its subscriptions over to the new project as well, in both the UI flow and the REST API flow.

I'd expect the data-layer connector to grow a helper along the lines of `CopyProjectSubscriptions(oldProjectId, newProjectId)` that the copy flow can call alongside the existing vars/aliases copying.
