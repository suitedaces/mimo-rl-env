## VerifyCommitLight / VerifyCommitLightTrusting accept commits with invalid signatures

While reviewing how a light client behaves against a malicious peer, I tried to feed it a commit where the voting power adds up correctly (>2/3 of the validator set) but the signatures themselves are garbage — I just replaced each `Signature` byte slice with random bytes of the right length, leaving everything else (validator addresses, block ID, height, etc.) intact.

I expected `ValidatorSet.VerifyCommitLight` (and `VerifyCommitLightTrusting`) to reject this commit, since none of the signatures actually verify against the corresponding validator pubkeys.

Instead, both functions return `nil` — i.e. the commit is accepted as valid.

Minimal sketch of what I'm doing:

```go
// build a normal valset + commit where 2/3+ of validators "sign" the block
vals, privVals := types.RandValidatorSet(4, 10)
commit := makeCommit(blockID, height, round, vals, privVals, chainID, time)

// now corrupt every signature
for i := range commit.Signatures {
    commit.Signatures[i].Signature = tmrand.Bytes(64)
}

err := vals.VerifyCommitLight(chainID, blockID, height, commit)
// err == nil  ❌  — I expected this to fail
```

The same thing happens with `VerifyCommitLightTrusting` when the voting power threshold is met by the (corrupted) signatures.

`VerifyCommit` (the full one used by consensus) does seem to catch this — it's only the two light-client variants that let it through. That's pretty bad: a light client is supposed to be the thing protecting users from exactly this kind of forged commit, and right now any peer that knows the validator set composition can hand it a commit that looks well-formed but contains no real signatures at all.

It would also be nice to have test coverage for "commit has enough voting power but signatures are invalid" on these light-client paths so this doesn't regress.
