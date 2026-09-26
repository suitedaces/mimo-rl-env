ENH: option to check merge is one-to-one, many-to-one, one-to-many, or many-to-many
In my experience, there are few places in data work where problems with data are more evident than when merging datasets -- something that is both a problem (if you think you're doing a one-to-one merge and one of the keys isn't unique in one dataset, you can introduce huge problems) and an opportunity (checking that a merge works as expected is a great way to catch problems). 

With that in mind, I'd like to propose adding a `check_merge` argument that accepts strings `one_to_one`, `one_to_many`, `may_to_one`, and `many_to_many`. If one of those strings is passed, the `merge` function would then check uniqueness of merge variables before running the merge, and if for example the merge key for the first dataset has duplicates in a `one_to_many` merge, it would throw an (informative) exception. 

(Stata made a similar move to bake this functionality into its merge command around Stata 12 using `1:1`, `1:m`, `m:1` syntax, which I'm also open to). 

Though this functionality can be replicated with user tests, it gets tiring to write them every time...
