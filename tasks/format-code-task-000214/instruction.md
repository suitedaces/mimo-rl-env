# Strengthen multi-shop authorization in the employee context

In the back office, the employee context already tells us whether the logged-in
employee is allowed to work on a given shop or on a given shop group. In a
multistore installation that is not enough: some operations target *all* shops
at once (the "all stores" context), and other code needs to resolve an
authorization decision directly from a shop constraint without having to branch
on its kind every time. Right now there is no way to ask the context either of
those questions, which lets employees act on the whole installation even when
they are only associated with a subset of its shops.

Extend the employee context with two new capabilities.

**1. "Is this employee authorized for the whole installation?"**

Add a way to ask whether the current employee has authorization for *all* the
shops that exist in the installation:

- If there is no logged-in employee, the answer is `false`.
- A super administrator is always authorized for all shops.
- Otherwise the employee is authorized for all shops only when they are
  authorized on every single shop that exists in the installation. If even one
  existing shop is outside their associated shops, the answer is `false`.
  Being associated with extra shops that no longer exist does not matter.

For this to be answerable, the context needs to know which shops exist. The
complete list of existing shop ids must be supplied to the context when it is
built, in addition to the employee. The current way of constructing the context
with the employee alone must keep working unchanged; when no shop list is
supplied the context behaves as if the installation contains no shops, so any
logged-in employee is trivially authorized for "all" of them.

**2. "Is this employee authorized for this shop constraint?"**

Add a way to resolve an authorization decision from a `ShopConstraint` value
object (`PrestaShop\PrestaShop\Core\Domain\Shop\ValueObject\ShopConstraint`):

- A constraint targeting a single shop is authorized exactly when the employee
  is authorized on that shop.
- A constraint targeting a shop group is authorized exactly when the employee
  is authorized on that shop group.
- A constraint targeting all shops is authorized exactly when the employee is
  authorized for all shops (as defined above).

These checks must stay consistent with the existing per-shop and per-shop-group
authorization rules (super administrators pass everything; a context with no
employee passes nothing).
