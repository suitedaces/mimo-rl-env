# Periodically clean up abandoned checkouts

Checkout objects pile up in the database forever. Shoppers start a checkout and never
finish, sessions get abandoned, and bots create empty carts that never receive a single
line. We need a recurring maintenance job that prunes stale checkouts so the table does
not grow without bound.

Add a background job, exposed as a Celery task named `delete_expired_checkouts` and
importable from the checkout app's tasks module
(`saleor.checkout.tasks.delete_expired_checkouts`), that deletes stale checkouts in a
single run. Calling it directly must perform the cleanup and must be safe to run at any
time (no error when there is nothing to delete).

A checkout is considered stale — and must be removed — when **any** of the following
holds, based on its last-change time:

- It has **no lines** and has not changed for longer than the *empty-checkout* retention
  window.
- It is **anonymous** (it has neither an email nor an assigned user) and has not changed
  for longer than the *anonymous-checkout* retention window.
- It has an **email or an assigned user** and has not changed for longer than the
  *user-checkout* retention window.

Checkouts that do not match any of these conditions must be left untouched.

The three retention windows must be configurable, with these defaults:

- empty checkouts: 6 hours
- anonymous checkouts: 30 days
- checkouts that carry an email or user: 90 days

Finally, wire the job into the project's periodic task schedule so it runs once a day.
