## AMP sensor doesn't see cross-repository dependencies when evaluating

I have my assets split across two code locations / repositories:

- `repo_upstream` defines `raw_data` (an upstream asset, materialized on some external schedule).
- `repo_downstream` defines `processed_data`, which depends on `raw_data`. I have an auto-materialize policy on `processed_data` that's supposed to gate on the parent — i.e. don't materialize `processed_data` if `raw_data` is missing / hasn't been materialized yet.

I set up an AMP sensor in `repo_downstream` whose `asset_selection` covers `processed_data` (and a few other downstream assets in the same repo), and let the asset daemon run it.

What I expected: the daemon evaluates `processed_data`, sees that its parent `raw_data` (which lives in the other repo) is missing, and skips materialization — same behavior I'd get if both assets lived in the same repo.

What actually happens: the AMP sensor behaves as if `raw_data` doesn't exist at all. The cross-repo parent relationship seems invisible to the evaluation, so the "wait for parent" rule never fires the way it should, and `processed_data` gets materialized at times that don't make sense relative to its real parent.

If I move both assets into the same repository, the AMP rules behave correctly and the parent dependency is respected. It only goes wrong once the parent and child live in different repos / code locations.

It seems like the AMP sensor evaluation is only looking at the assets within the sensor's own repository, instead of considering the full asset graph across the workspace when figuring out parent/child state. The selection of *which* assets the sensor is responsible for should still come from the sensor's `asset_selection`, but the dependency graph used to actually evaluate the policies needs to include assets from other code locations too.

Repro sketch:

```python
# repo_upstream/repo.py
from dagster import asset, Definitions

@asset
def raw_data():
    ...

defs = Definitions(assets=[raw_data])
```

```python
# repo_downstream/repo.py
from dagster import asset, AssetKey, AssetSelection, Definitions, AutoMaterializePolicy
from dagster._core.definitions.auto_materialize_sensor_definition import (
    AutoMaterializeSensorDefinition,
)

@asset(
    deps=[AssetKey("raw_data")],
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def processed_data():
    ...

amp_sensor = AutoMaterializeSensorDefinition(
    name="downstream_amp",
    asset_selection=AssetSelection.assets(processed_data),
)

defs = Definitions(assets=[processed_data], sensors=[amp_sensor])
```

With both repos loaded into the same workspace and `raw_data` never materialized, the AMP sensor still issues runs for `processed_data` as if it had no parent — instead of correctly waiting on `raw_data`.
