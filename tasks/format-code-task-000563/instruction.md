## Problem Statement

I keep getting checksum mismatch errors on my managed order book for tXRPBTC at P0 precision — the data from the server looks fine but it errors out anyway. The issue seems to show up around very small price values like 0.00001, but I don't have a clean way to inspect the book with the original string values to confirm. Can you help me get past this so I stop getting false checksum errors, and also give me a way to read the book with prices/amounts as strings instead of floats?

## Expected Outcomes

- Managed order book checksum validation should not emit checksum-mismatch errors for valid server order book data whose numeric values are precision-sensitive.
- `WSv2#getLosslessOB(symbol)` should return the currently managed order book for that symbol with order book prices and amounts preserved as the original string-form numeric values received from the websocket message.
- `WSv2#getLosslessOB(symbol)` should return `null` when no string-preserved managed order book is available for the requested symbol, such as before a managed snapshot exists or when order book management is not enabled.
- The existing managed order book API should continue to expose its normal numeric order book view for callers that use `WSv2#getOB(symbol)`.

## Implementation Notes

- The representation, parsing strategy, and update mechanism for preserving exact order book values are implementation details, as long as the public behavior above is satisfied.
- Checksum handling should remain compatible with the existing managed order book flow and should avoid changing unrelated websocket message behavior.
- Add or update public documentation for any new public API surface.
