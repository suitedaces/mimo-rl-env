events.tsv with same trial_type, but different value
I have some `events.tsv` files that look like this:

```
onset    	duration 	sample 	trial_type 	stim_file 	value
9.6211   	0.0      	9853   	response   	n/a       	202
15.1250  	0.0      	15489  	response   	n/a       	202
19.4121  	0.2      	19879  	stimulus   	n/a       	11
19.8926  	0.0      	20371  	response   	n/a       	201
20.8623  	0.2      	21364  	stimulus   	n/a       	12
21.3164  	0.0      	21829  	response   	n/a       	201
22.3779  	0.2      	22916  	stimulus   	n/a       	14
22.7969  	0.0      	23345  	response   	n/a       	201
```
As you can see, the `response` `trial_type` can either be associated with a `201` (correct) or `202` (incorrect) value.

When this file is read by MNE-BIDS, the distinction between the two types of response disappears, as we ignore the `value` column if we find a `trial_type` column.

There's a similar pattern for the `stimulus` trial type.

I would propose that in the case where we find that the `trial_type` <> `value` mapping is not unique, we create hierarchical event names composed of both fields, i.e. in this specific case, `response/201` and `response/202`.
Also we should make it easy for users to rename the events on the BIDS level.

Thoughts?

cc @sappelhoff @adam2392 @jasmainak @agramfort
