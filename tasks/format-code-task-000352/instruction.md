## Problem Statement

When I move a chassis to a different rack in Ralph, the blades under it still show the old rack afterward, which makes the location data inconsistent. Could you make the directly attached child assets follow the parent’s rack when I save that change?

## Expected outcomes

- When an existing parent data center asset is saved after its rack changes, each directly attached child data center asset reflects the parent’s new rack.
- Child assets that are not directly attached to the moved parent are outside the required synchronization scope.
- Saving a parent without changing its rack should not introduce unrelated location changes.

## Implementation notes

- The specific place where the synchronization is performed is up to the implementation, as long as the externally observable saved asset state is consistent afterward.
- Preserve existing validation and save behavior for data center assets while adding the rack synchronization behavior.
