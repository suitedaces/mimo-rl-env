## Confusing error when clicking "+" on a cart line that used a voucher

I'm a customer of a pretix shop. The flow I hit:

1. The shop has a product that requires a voucher (it's hidden until you redeem one). I get a voucher link, open it, and add one ticket to my cart. Cart line shows up with the voucher code under it — fine.
2. The voucher in this case has only one redemption left (let's say `max_usages=1`, so after my first ticket the voucher is fully redeemed).
3. I now want to buy a second ticket for a friend. The voucher itself is single-use, so I'm fine paying the regular price for the second one. I click the "+" button next to the line in the cart.

What happens: I get an error, but it's the wrong / confusing one. For a `require_voucher` (or `hide_without_voucher`) product I get something like *"You need a valid voucher code to order this product"*, which makes no sense — I just used a voucher to add the first one, and the message has nothing to do with the actual situation, which is that the voucher is already fully redeemed. For a regular product I just get refused outright instead of getting a second ticket at the normal price.

What I'd expect when clicking "+" on a cart line that has a voucher attached:

- If the voucher still has redemptions left, sure, use it again (current behavior is fine).
- If the voucher is already at its usage limit, the "+" button shouldn't be a dead end. For a normal product, just add another one at the standard price — I'm clearly trying to buy one more. For a product that genuinely can't be sold without a voucher, the error I see should match reality ("this voucher code has already been used the maximum number of times allowed") rather than telling me I need a voucher.

The "+" UI implies "give me one more of this", and it currently breaks in a non-obvious way precisely in the voucher case where users are most likely to click it.

(Implementation hint for whoever picks this up: the cart-add endpoint will probably need to accept a new opt-in flag alongside the existing `_voucher_code` field — something like `_voucher_ignore_if_redeemed=on` — so the "+" button can say "try this voucher, but silently fall back to no-voucher if it's already fully redeemed" instead of the normal hard-fail-on-exhausted-voucher behavior.)
