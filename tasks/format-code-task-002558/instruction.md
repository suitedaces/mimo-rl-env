## Draft orders get linked to users on registration / existing orders aren't matched up

We hit two related issues around `match_orders_with_new_user` and historical order data:

**1. Draft orders are being attached to customer accounts**

Our staff often creates a draft order in the dashboard ahead of time (e.g. preparing an order over the phone) and fills in the customer's email on the draft. If that customer later signs up using the same email, the still-in-progress draft order ends up linked to their account — it shows up in their order history even though we haven't finalized it yet.

Drafts are internal work-in-progress; they shouldn't be tied to a user account until they become a real order. Only confirmed/real orders should be picked up when a new user registers.

**2. Historical orders placed before registration aren't picked up**

Separately, we have plenty of orders in production that were placed as guests (so `user_email` is set but `user` is `NULL`). For accounts that were created later with the matching email, those past orders never got associated — they're orphaned in the DB, while newer ones placed after registration are properly linked.

It would be great if existing data could be reconciled so that real (non-draft) guest orders get attached to the matching user accounts retroactively, and so that going forward draft orders are excluded from this auto-matching.
