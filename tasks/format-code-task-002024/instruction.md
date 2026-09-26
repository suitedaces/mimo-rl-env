### Environment
* Nautobot version: current `develop`

### Proposed Functionality
Add a Bulk Edit action for the **Rack Group** model in the web UI, the same way most other DCIM models (Racks, Locations, Power Panels, Device Types, etc.) already expose one.

### Use Case
We manage a fairly large number of rack groups across multiple sites. Today, when we need to update something common across many rack groups (for example, cleaning up or normalizing descriptions after a migration), the Rack Group list view does not offer a bulk edit option — only bulk delete. The only way to update N rack groups is to open each one individually and edit it, which is tedious and error-prone at scale.

Every comparable model in DCIM already has a "Edit Selected" action on its list view, so the absence of one on Rack Groups feels like an oversight rather than an intentional choice. It would be great if Rack Groups supported the same bulk edit workflow as the rest of the DCIM models, so that selecting multiple rack groups in the list view exposes an "Edit Selected" button that lets us update the common editable fields in one shot.

### Database Changes
None expected — this is just exposing bulk edit over existing fields.

### External Dependencies
None.
