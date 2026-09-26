## Step 3: stop creating a Vercel deploy webhook during installation

Follow-up to the migration plan tracked in #26185. Steps 1 and 2 added a Sentry-side endpoint that can receive Vercel deployment events directly, so we no longer need to register a webhook on Vercel's side when a user installs the integration.

### What needs to change

When a user installs the Vercel integration from this point on, the install flow should **not** call out to the Vercel API to create a deploy webhook anymore. As a consequence, freshly installed integrations should also no longer carry a `webhook_id` in their metadata (since there's no webhook being created to record an id for).

### Backward compatibility

Integrations that were installed **before** this change will keep working as-is — we are not touching their existing Vercel-side webhook or stripping anything from their stored metadata. During the transition, those older installations will receive deployment events twice (once via the old Vercel webhook, once via the new endpoint). That's expected and acceptable for now.

We need to be able to tell new installs apart from pre-existing ones later, so the convention going forward is: **the presence or absence of `webhook_id` in the integration metadata is what distinguishes an old install from a new one.** Old installs have it, new installs don't. Please make sure that distinction holds after this change.

### Out of scope

- Anything related to deduping events for users who fall into the transition window (double-delivery is acceptable).
- Backfilling or migrating existing installations.
- Removing the now-unused webhook-receiving code on the Vercel side — we will clean that up in a later step once enough time has passed.
