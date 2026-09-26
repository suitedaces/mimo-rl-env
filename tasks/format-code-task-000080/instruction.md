# Harden the hsm_secret tool's `encrypt` flow and file validation

Our standalone HSM secret command-line utility (`tools/hsmtool`) lets operators
encrypt and decrypt their node's `hsm_secret` file with a password. Two rough
edges keep biting people, and I'd like both fixed.

## 1. Confirm the password when encrypting

Right now `encrypt <path/to/hsm_secret>` asks for the password exactly once and
immediately encrypts the seed with it. A single typo means the operator locks
themselves out of a seed they can never recover.

Make the `encrypt` subcommand ask for the password a second time to confirm it,
the way well-behaved tools do. The behavior must be:

- The two entries must match. If they differ, the tool aborts with a non-zero
  exit status, prints an error that makes clear the confirmation did not match,
  and leaves the `hsm_secret` file **completely untouched** (still the original
  plaintext seed, same bytes, same size).
- If the two entries match, encryption proceeds exactly as before, producing a
  valid encrypted `hsm_secret` that `decrypt` can later turn back into the
  original seed using the same password (a full encrypt → decrypt round-trip
  must recover the original bytes).

## 2. Be strict about what counts as a valid `hsm_secret`

A plaintext seed is exactly 32 bytes and an encrypted one is exactly 73 bytes.
Today the tool only checks "bigger than 32 means encrypted", so files of any
other length get misinterpreted (treated as encrypted, or partially read) and
produce confusing failures.

Whenever a subcommand needs to read an existing `hsm_secret` (for example
`encrypt` and `decrypt`), it must first reject any file whose size is neither 32
nor 73 bytes. Rejection means: print an error that identifies the file as an
**invalid** `hsm_secret`, exit with a non-zero status, and leave the file
unchanged. A genuine 32-byte plaintext seed and a genuine 73-byte encrypted seed
must keep working exactly as they do today.

Passwords are read from the terminal with echo disabled, as before.
