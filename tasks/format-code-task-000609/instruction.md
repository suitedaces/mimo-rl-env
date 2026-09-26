### What can be improved?

Being able to load tabular data is a wonderful new feature.
But it is currently limited by forcing the data to 'match' calliope's dimension names in certain cases. Enforcing strict naming by default makes a lot of sense: you avoid ambiguity and you also avoid the risks of relying on column position.

However, it will often be too inflexible.

## Reasoning

Some of our names might lead to files being less human readable, or finicky: 
- if a model is national resolution, `nodes` is less informative than `country`
- people will often go for `technology` or `tech` instead of `techs`, since it can be intuitive to name columns in singular
- people might prefer `time` or `utc_timestamp`, over `timesteps`...

This will lead to a lot of 'boilerplate' code that just shapes the data to fit Calliope's naming. See the following 3 examples for different names used for timeseries in Euro Calliope with v6.10:

![image](https://github.com/user-attachments/assets/d3e2f638-3a36-4005-81da-781653cd9f7e)
![image](https://github.com/user-attachments/assets/73b95df4-59f0-42a3-b9b8-c9e8c4c64833)
![image](https://github.com/user-attachments/assets/fed11440-0a8b-425b-88a0-345ba2a49edc)

All 3 are equally 'human' readable, but since they do not specify `timesteps`, they won't load into Calliope.

# Proposal

An option to use mappings would solve this issue.
For example, you could load one of the timeseries above this way:

```
data_sources:
  demand_elec_timeseries:
    source: timeseries/demand/electricity.csv
    columns: nodes
    rows: {timesteps: time}
    add_dims:
      techs: demand_elec
      parameters: sink_use_equals
```

This is still strict, but more flexible.

### Version

v0.7.0.dev3

---

A new top-level data-source option (something like `rename_dims`) that takes a `{old_name: new_name}` mapping would be a natural fit here.
