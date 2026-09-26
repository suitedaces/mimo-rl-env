I'm seeing an issue after `clusterctl move` where my already-provisioned BareMetalHosts come up in the new management cluster like they're fresh hosts and BMO starts discovery/inspection again. These hosts were paused before the move, so I expected CAPM3/BMO to preserve enough state for them to resume as already provisioned instead of poking the hardware again. Can you fix the move/pause flow so migrated BMHs don't get re-inspected unnecessarily?

Expected outcomes:
- Pause/move preservation: when CAPM3 prepares a BareMetalHost for migration, the migrated object should carry the BMO-recognized host state needed for the target management cluster to resume it as already provisioned.
- Pause compatibility: the host should remain visibly paused during the move, and existing pause behavior for already-paused hosts should continue to work.
- Failure classification: failures while preparing or updating the paused host state should be surfaced as update-related machine errors rather than create-related ones.

Implementation notes:
- Preserve the existing pause behavior while ensuring migrated, already-provisioned hosts retain restorable state.
- The exact validation location, serialization mechanism, and code organization are up to the implementer; tests should validate the resulting BareMetalHost state and Metal3Machine error classification, not internal helper structure.
