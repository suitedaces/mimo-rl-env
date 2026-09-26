### Feature: filter contact assignments by the contact's group

I organize my contacts into contact groups by team (e.g. *Network Ops*, *Security*, *Datacenter Smart Hands*). When I want to see what a team is on the hook for, the natural query is "give me all contact assignments where the assigned contact belongs to group X".

On the Contact endpoint this works fine — I can pull contacts in a group with something like `/api/tenancy/contacts/?group_id=5` (or by slug). But the equivalent doesn't exist on the ContactAssignment endpoint. Hitting `/api/tenancy/contact-assignments/?group_id=5` just returns everything, the parameter is silently ignored.

Today the workaround is two round trips: first list every contact in the group, then list assignments filtered by each `contact_id`. That gets unwieldy quickly for larger groups and it's annoying to do from the UI filter panel too, where there's just no "Contact group" option to pick from on the contact assignments list.

It would be great if the contact-assignments filter set understood "contact group" as a first-class filter, the same way the contacts list already does. Then I could go straight from "which team" to "what they're assigned to" in one query, both via the REST API and via the list view filters.
