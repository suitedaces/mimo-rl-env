### dataapi `/metrics` returns incorrect `total_stake`

Hitting the `/metrics` endpoint on the data API and reading `total_stake` / `total_stake_per_quorum`, the numbers don't match what's actually staked on-chain. The on-chain totals are way larger than what `uint64` can hold, and the values coming out of the API look like they've wrapped/been truncated.

Looking at the `Metric` response struct, `TotalStake` and `TotalStakePerQuorum` are typed as `uint64`, which isn't wide enough for real total-stake values. These fields need to be able to represent arbitrarily large integers so the reported totals are actually correct.

Could the metrics handler be updated so the total stake values it computes and serializes can hold the full on-chain values?
