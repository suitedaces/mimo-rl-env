## Problem Statement

When I open an AOPP link while my BitBox is already connected and unlocked, the wallet jumps straight into picking an account, which feels a bit too automatic. I’d like it to pause first and show me who is asking, with a chance to continue or cancel before I get taken further into the flow.

## Expected outcomes

- AOPP requests opened while a keystore is already connected must first enter a visible approval step instead of immediately continuing to account selection.
- The approval step must expose the request host and provide both Cancel and Continue actions.
- The AOPP state returned to clients must include `state: 'user-approval'` while the request is waiting for this explicit decision.
- Calling `POST /aopp/approve` must approve an AOPP request that is currently waiting for user approval and then let the normal AOPP flow continue to the next appropriate state.
- Calling `POST /aopp/approve` when the AOPP flow is not waiting for user approval must not advance the flow.
- The web AOPP API should expose `approve(): Promise<null>` for the Continue action, while the existing cancel behavior remains available for Cancel.

## Implementation notes

- The exact internal state-machine structure, handler wiring, and UI component organization are up to the implementer.
- Preserve existing AOPP behavior for requests that still need a keystore to be connected or unlocked.
- Validate the behavior through externally observable state transitions, API responses, and UI actions rather than relying on internal naming.
