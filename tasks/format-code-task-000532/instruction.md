# Confirmable wallet transactions

Today a deposit or withdrawal can be recorded as *unconfirmed* by passing `false` as the
third argument to `deposit(...)` / `withdraw(...)` (and their `force*` variants). An unconfirmed
transaction is persisted, exposes `confirmed === false`, but it intentionally does **not** affect
the wallet balance. What's missing is a way to *later* confirm such a pending transaction.

Please add the ability to confirm a previously-recorded transaction on the wallet it belongs to.

Expected behaviour:

- A wallet exposes a `confirm($transaction)` method. Confirming a still-unconfirmed transaction
  applies its amount to that wallet's balance (a deposit increases it, a withdrawal decreases it),
  flips the transaction's `confirmed` flag to `true`, and returns `true`.

- A transaction may only be confirmed through the wallet it was recorded against. Trying to
  confirm it through any other wallet must be rejected, and no balances may change.

- A transaction that is already confirmed cannot be confirmed again. The attempt must be rejected
  and the balance left untouched (the transaction stays confirmed).

- Confirming a withdrawal must respect the wallet's available funds: if applying it would make the
  balance go negative, the confirmation must be rejected and the balance left unchanged (the
  transaction stays unconfirmed).

- A rejected `confirm($transaction)` raises an exception. Alongside it, provide a
  `safeConfirm($transaction)` method that performs the exact same confirmation but returns `false`
  instead of raising when the transaction cannot be applied, again without changing any balance.

The existing deposit/withdraw behaviour, including how unconfirmed transactions are created, must
stay exactly as it is.
