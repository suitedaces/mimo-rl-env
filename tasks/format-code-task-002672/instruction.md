simple specification of unitful quantities in config files
We need an easy way to specify numbers with units in the config files. Currently those need to be constructed manually:

```yaml
survey_area: !astropy.units.Quantity '1000 deg2'
```

This can be simplified in the first instance by registering a custom `!quantity` tag that does the construction:

```yaml
survey_area: !quantity '1000 deg2'
```

After which we can register a custom resolver that matches values that look like `number + string` to the `!quantity` tag:

```yaml
survey_area: 1000 deg2
```
