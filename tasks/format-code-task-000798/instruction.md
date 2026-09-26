## NNS init CSV parser no longer accepts `dissolve_delay_s` / `maturity_e8s_equivalent`

I'm using `add_all_neurons_from_csv_file` to bootstrap NNS governance with a set of initial neurons (similar to `rs/nns/integration_tests/src/neurons.csv`). I want each neuron in that CSV to have a configurable dissolve delay and an initial maturity.

When I add `dissolve_delay_s` and `maturity_e8s_equivalent` columns to the CSV header, init blows up on the header check — the parser only accepts the fixed 6-column schema (`neuron_id;owner_id;created_ts_ns;staked_icpt;follows;not_for_profit`) and rejects anything else.

If I drop those columns and stick to the 6-column schema, init succeeds, but then every neuron ends up with a dissolve delay of 1 second regardless of what I wanted, and maturity is always 0. So there's currently no way to configure these two per-neuron values from the CSV at all.

This used to be supported (or at least the field names suggest it was intended to be), so it feels like a regression. Could the CSV format be updated so that `dissolve_delay_s` and `maturity_e8s_equivalent` are recognized again and actually flow into the resulting `Neuron`? The committed `neurons.csv` test fixture should also be updated to match.
