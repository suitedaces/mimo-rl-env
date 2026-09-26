Complete the backend Organizations API so server-side SDK users can administer organizations, memberships, and invitations without dropping down to a custom fetcher. The shared types and browser-side resources already model these concepts, but `@clerk/backend-core` currently exposes only organization creation.

Add typed Promise-returning methods on `clerk.organizations` with these signatures and wire behaviors:

- `getOrganizationList({ limit?, offset? }?)`: `GET /organizations`.
- `getOrganization(organizationId)`: `GET /organizations/:organizationId`.
- `updateOrganization(organizationId, { name })`: `PATCH /organizations/:organizationId` with `{ name }`.
- `deleteOrganization(organizationId)`: `DELETE /organizations/:organizationId`.
- `getOrganizationMembershipList({ organizationId, limit?, offset? })`: `GET /organizations/:organizationId/memberships`.
- `createOrganizationMembership({ organizationId, userId, role })`: `POST /organizations/:organizationId/memberships` with `user_id` and `role`.
- `updateOrganizationMembership({ organizationId, userId, role })`: `PATCH /organizations/:organizationId/memberships/:userId` with only `role`.
- `deleteOrganizationMembership({ organizationId, userId })`: `DELETE /organizations/:organizationId/memberships/:userId`.
- `getOrganizationInvitationList({ organizationId, limit?, offset? })`: `GET /organizations/:organizationId/invitations`.
- `createOrganizationInvitation({ organizationId, emailAddress, role, redirectUrl? })`: `POST /organizations/:organizationId/invitations` with `email_address`, `role`, and `redirect_url` only when supplied.
- `revokeOrganizationInvitation({ organizationId, invitationId })`: `POST /organizations/:organizationId/invitations/:invitationId/revoke`.

Only `limit` and `offset` belong in list query strings. When neither is supplied, emit no query string at all; path identifiers must not leak into the query or body. Membership and invitation roles are the existing closed union `'admin' | 'basic_member'`, not arbitrary strings.

Return the existing `Organization` resource from organization operations. Add and publicly export `OrganizationMembership` and `OrganizationInvitation` resource classes from the backend-core package root. Membership JSON must become an object with `id`, `role`, numeric `createdAt`/`updatedAt`, a nested `Organization`, and camel-cased `publicUserData` containing `userId` from `public_user_data.user_id`, `firstName`, `lastName`, `profileImageUrl`, and `identifier`. Invitation JSON must expose `id`, `organizationId`, `emailAddress`, `role`, `status`, and numeric `createdAt`/`updatedAt`. As with the existing backend resources, unrelated top-level response fields must not become public resource properties.

Every operation that takes an organization ID must reject an empty ID with the existing `A valid ID is required.` error before issuing a request. Membership mutations must independently validate `userId`, and invitation revocation must independently validate `invitationId`, with the same fail-fast behavior. Preserve the existing `createOrganization({ name, createdBy })` request and response behavior.
