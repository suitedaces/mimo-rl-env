## Problem Statement

When I tweak an ACL via ModifyACL and the interface list barely changes (or doesn't change at all), I can see in the VPP calls that it still unbinds every old interface and rebinds every new one — so untouched interfaces get a pointless remove+add round trip. On a busy box this causes noticeable churn for what should be a no-op on those interfaces. Could ModifyACL be smarter and only touch the interfaces that actually differ between the old and new ACL, and just skip the VPP calls entirely when the binding set hasn't changed?

## Expected outcomes

- ACL interface binding changes made through `ModifyACL` should be incremental: interfaces that remain bound in both the old and new ACL should not be removed and re-added.
- Interfaces removed from the ACL should be unbound, and interfaces newly added to the ACL should be bound, with ingress and egress bindings handled according to their respective ACL interface lists.
- If the ACL’s effective interface bindings are unchanged, `ModifyACL` should avoid issuing interface-binding VPP operations for that update.
- Empty added/removed binding groups should be treated as no-ops rather than as operations to send onward.

## Implementation notes

- The specific data structures, helper functions, and placement of the comparison logic are up to the implementer.
- The change should preserve existing ACL modification behavior outside of avoiding redundant interface binding churn.
- Tests should validate externally observable VPP binding operations rather than relying on a particular internal helper or intermediate representation.
