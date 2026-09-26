## Feature request: ability to remove an already-applied voucher from the cart

We're building a checkout flow on top of flamingo-commerce. Customers can enter a coupon code and we call the existing `ApplyVoucher` flow (`/api/cart/applyvoucher`) to attach it to the cart — that works fine, and the applied codes show up under `cart.AppliedCouponCodes` so we can render them in the cart summary.

The problem is the inverse operation. A pretty standard piece of cart UX is "here are the vouchers you've applied, click the X to remove this one" — e.g. the customer pasted the wrong code, or got handed a better promo and wants to swap. Today there's no way to do that from the cart API: I can keep adding codes, but I can't take one back off without throwing the whole cart away.

I'd expect removing a voucher to be a first-class cart mutation, on the same level as applying one — you say "drop this code from the cart", and afterwards the cart no longer lists it and any discount tied to it is gone. It should be reachable via the cart API so the storefront/JS layer can call it directly, and it should flow through the same modify-behaviour layering that `ApplyVoucher` uses (so the in-memory adapter we use in tests/dev keeps working, and other adapters can implement it the same way).

Would it be possible to add this? Naming-wise I'd expect the new operation to mirror `ApplyVoucher` (something like `RemoveVoucher` on the cart service / modify-behaviour).
