# Reverse lookup for linked addresses

WeaveDB lets a dapp user link throwaway "disposable" addresses to their main
account so they can auto-sign writes without prompting a wallet for every
action. Today the client can resolve a single disposable address to the account
it points at via `getAddressLink(address)`, which returns `{ address, expiry }`.

There's no way to go the other direction. Given an account, we want to know
which disposable addresses are currently linked to it — e.g. to show a user
every auto-signing key tied to their wallet, or to revoke them.

Add a reverse lookup to the client for the BPT contract. Expose it as
`getAddressLinks(account)` (the plural counterpart of `getAddressLink`), a read
that returns the list of disposable addresses currently linked to `account`.

Expected behavior:

- It returns an array of the disposable addresses currently linked to the given
  account. When the account has nothing linked to it, it returns an empty array
  (`[]`).
- Creating a link (`createTempAddress` / `addAddressLink`) makes the new
  disposable address appear in its target account's list; removing the link
  (`removeAddressLink`) makes it disappear again.
- The list never contains duplicates, and entries for one account never leak
  into another account's list.
- Account matching follows the same convention as `getAddressLink`: Ethereum
  addresses are matched case-insensitively.
- Ordering of the returned array is not significant.

The reverse lookup must stay correct across any sequence of link additions and
removals — it should always reflect exactly the set of links that
`getAddressLink` would currently resolve back to that account.
