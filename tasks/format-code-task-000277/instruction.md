## Problem Statement

I'm integrating the ERC-6551 account with a standard signer check, and calling `isValidSigner(address,bytes)` on the TBA just fails / isn't exposed, so I can't verify whether a given address is treated as a valid signer.

## Expected outcomes

- ERC-6551 accounts expose the standard `isValidSigner(address signer, bytes calldata context) -> bytes4` query through their public ABI.
- Calling `isValidSigner` with an address that the account treats as a valid signer returns the EIP-6551 `isValidSigner` magic value.
- Calling `isValidSigner` with an address that the account does not treat as a valid signer returns a non-magic failure value rather than reporting the address as valid.
- The `context` argument can be supplied by standard callers without causing the public signer check entrypoint to fail merely because the entrypoint is missing.

## Implementation notes

The exact internal mechanism used to determine signer validity is up to the implementation, but the externally observable behavior must match the ERC-6551 signer-check contract interface. Existing account behavior unrelated to the signer check should remain unchanged.
