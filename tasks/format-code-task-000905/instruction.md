ValueError when analyzing non-malicious APKs with new rule weights
**Describe the bug**

In quark-engine/quark-rules#38, we introduced new rule weights for detecting DroidKungFu. While Quark analyzes DroidKungFu samples correctly with these weights, it raises a ValueError when analyzing non-malicious APKs.

I use [InsecureBankv2.apk](https://github.com/quark-engine/apk-samples/blob/master/vulnerable-samples/InsecureBankv2.apk) (`b18af2a0e44d7634bbcdf93664d9c78a2695e050393fcfbb5e8b91f902d194a4`) as an example here. When analyzing it with the new rule weights, Quark raises the following ValueError.

```shell
Traceback (most recent call last):
  File "/mnt/storage/quark-engine/quark/cli.py", line 458, in <module>
    entry_point()
  File "/mnt/storage/quark-engine/.venv/lib/python3.12/site-packages/click/core.py", line 1442, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/storage/quark-engine/.venv/lib/python3.12/site-packages/click/core.py", line 1363, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/mnt/storage/quark-engine/.venv/lib/python3.12/site-packages/click/core.py", line 1226, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/storage/quark-engine/.venv/lib/python3.12/site-packages/click/core.py", line 794, in invoke
    return callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/storage/quark-engine/quark/cli.py", line 344, in entry_point
    print_warning(w.calculate())
                  ^^^^^^^^^^^^^
  File "/mnt/storage/quark-engine/quark/utils/weight.py", line 52, in calculate
    raise ValueError("Weight calculate failed")
ValueError: Weight calculate failed
```

**To Reproduce**

1. Install Quark
```shell
pip install -U quark
```
2. Apply the new rule weights to the Quark default ruleset.
```shell
git clone https://github.com/haeter525/quark-rules.git -b add_rule_for_droidkungfu /tmp/quark-rules
cp -r /tmp/quark-rules/rules ~/.quark-engine/quark-rules/
```
3. Download [the APK](https://github.com/quark-engine/apk-samples/blob/master/vulnerable-samples/InsecureBankv2.apk) and run Quark analysis.
```shell
quark -a InsecureBankv2.apk -s
```

**Root Cause**
The root cause is that Quark uses the [Weight.calculate()](https://github.com/quark-engine/quark-engine/blob/d4493b3b2e686298a8ee4bda6841f1327ed671ce/quark/utils/weight.py#L21) function to determine an APK’s risk level based on its score. However, this function was not designed to handle negative scores, so it raised a value error.
