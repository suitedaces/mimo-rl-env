Allow pinning of increments
Thank you for building `bumpver`. I really like using it.

I'm using a version pattern `YYYY.MM.INC1`. This generates versions like `2022.11.1`, `2022.11.2`, `2022.12.1`.

I recently ran into the case where I needed to make a hotfix release for one of the versions. My initial thought was to just increment the `INC1` part (and that's what I did in the end, due to the "missing" feature requested in here).

But thinking further, what I would've liked more, was a "hotfix" increment, resulting in e.g. `2022.11.2-1`. My approach was to add `[-PATCH]` to the version pattern: `YYYY.MM.INC1[-PATCH]`.

However, when running `bumpver update --patch`, I ended up with `2022.11.3` instead of `2022.11.2-1`.

Looking into the `--help` for `update`, I spotted `--pin-date`. With a version pattern `YYYY.MM.DD[-PATCH]` the command worked as expected. But with `INC1` instead of `DD` it did not. 

My understanding is, that the increment just can't be pinned. Thus, I'm requesting to add this feature.
