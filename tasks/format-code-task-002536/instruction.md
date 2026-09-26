## Editing a Kraken event to use a custom asset breaks history events retrieval

I have some events imported from Kraken. For one of them, I wanted to change the asset to a custom asset I had defined in rotki (not a token from any of the supported chains, just a manually-added asset I track separately).

After editing the event and switching its asset to the custom one, the Kraken history events stop loading properly — the history events view for Kraken is broken from that point on. Reverting the event back to a regular asset makes things work again.

The edit itself goes through fine, it's only when rotki tries to fetch / display the events afterwards that things go wrong. Custom assets work fine in other places (manual balances, etc.), so I'd expect them to be usable on Kraken events too without breaking the events list.
