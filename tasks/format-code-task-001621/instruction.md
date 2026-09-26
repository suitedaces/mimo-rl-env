Unable to fetch author of PR without re-fetching PR as an Issue
Neither `Pull` nor `Pull.Smart` expose a method to get the author of the pull request, even though this data is in the pull request JSON (as the `user` member; see https://developer.github.com/v3/pulls/#get-a-single-pull-request). To get such data, one must currently do `pull.issue().author()`, which does an unnecessary/wasteful network request to re-fetch the PR as an Issue.
I suggest adding such a method.
