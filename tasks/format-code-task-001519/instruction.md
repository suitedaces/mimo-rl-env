# Problem Statement

I'm trying to manage a MUC from aioxmpp and I need to see which JIDs currently have a given affiliation in the room, like owners or members, instead of only being able to set them. I also want to set the room's vCard/avatar, but `set_vcard` seems to only target my own account right now. Could you add support for those MUC admin use cases, ideally with a small example showing how to do it?

# Expected Outcomes

- MUC affiliation lookup: the MUC service exposes a public async `get_affiliated` API which takes a room JID and an affiliation name, queries that room, and returns the JIDs reported by the room for that affiliation.
- MUC affiliation lookup errors: authorization or server errors raised while querying affiliations are propagated through the normal aioxmpp IQ error path.
- Foreign vCard writes: `aioxmpp.vcard.Service.set_vcard` accepts an optional `jid` keyword argument; when supplied, the vCard update targets that entity so callers can update a MUC or other foreign entity vCard.
- Existing vCard behavior: calling `aioxmpp.vcard.Service.set_vcard(vcard)` without `jid` continues to update the connected account's own vCard, preserving compatibility with existing callers.
- Examples and documentation: include small examples named `get_muc_affiliations.py` and `set_muc_avatar.py`, and mention the new MUC affiliation lookup and targeted vCard update capabilities in the changelog or equivalent user-facing documentation.

# Implementation Notes

- Follow the existing aioxmpp service conventions for asynchronous APIs, IQ submission, errors, and examples.
- The exact internal helper structure and validation placement are up to the implementation, as long as the public API behavior above is satisfied.
- Keep the existing public behavior of unrelated MUC and vCard operations unchanged.
