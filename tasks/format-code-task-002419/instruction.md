## Add `base16` and `base32` validators to the `encoding` module

I'm using `validators` for input validation in a small service and ran into a gap.

The library already has `validators.base58` and `validators.base64` under the `encoding` module, which is great — I'm using them to sanity-check user-supplied encoded strings before passing them to the rest of the pipeline. However, two of the most common encodings I deal with don't seem to have a counterpart:

- **base16** — I get a lot of hex-encoded inputs (hash digests, raw byte dumps that are pasted in as hex strings, etc.) and I'd like a one-liner to confirm a string really is a valid hex/base16 encoding before I try to decode it.
- **base32** — I also handle things like TOTP / 2FA secrets and some token formats that are base32-encoded, and right now I have to roll my own check or rely on `try/except` around a decode call, which feels inconsistent with how I'm validating the other encodings.

Concretely, today I have to do something like this for the cases that aren't covered:

```python
import validators

# These work nicely:
validators.base58(some_btc_like_string)
validators.base64(some_b64_string)

# But for these I currently have no equivalent:
# validators.base16(some_hex_string)
# validators.base32(some_totp_secret)
```

It would be great if the `encoding` module exposed `base16` and `base32` validators alongside the existing `base58` / `base64` ones, with the same calling convention and the same True / `ValidationError` return behavior, so all four encodings can be validated in a uniform way.

Happy to help test if useful.
