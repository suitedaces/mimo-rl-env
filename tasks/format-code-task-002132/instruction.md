## `MergeStructs` / `MergeStructInto` should support overwriting destination values

I'm using `ygot.MergeStructs` (and `MergeStructInto`) to combine two `ValidatedGoStruct`s of the same type — think a baseline config plus an override layer that should "win" where it sets something.

Currently, if the same leaf is set in both structs to different values, the merge fails with an error along the lines of "destination value was set, but was not equal to source value when merging ptr field". The same happens for enum fields and for interface-typed (union) fields when both sides are populated with non-equal values.

That makes sense as a safe default — you don't want to silently clobber data — but in my use case the whole point is that the second struct represents an intentional override. I want any field that's set on the source side to replace the value on the destination side, while fields that are unset in the source should leave the destination untouched.

Right now I'd have to walk the override struct myself and null out every conflicting field on the base before calling `MergeStructs`, which defeats the purpose of having the merge helper.

Could `MergeStructs` / `MergeStructInto` grow an opt-in way to enable "source overwrites destination" semantics? The default behaviour (error on conflict) should stay the same so existing callers aren't affected.

I'm imagining the opt-in surface as something like a variadic `MergeOpt` interface on these functions, with a marker option (e.g. `MergeOverwriteExistingFields`) that callers pass in to switch on the overwrite behaviour.
