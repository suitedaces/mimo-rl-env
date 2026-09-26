# Make Twitter share verification resilient to retweets and attached media

Our bridge server verifies social "promotion" actions. For Twitter, an incoming
webhook event is checked against the exact content a user was asked to share: a
`SHARE` action is considered valid only when the tweet text — after Twitter's
automatic transformations are undone — matches the expected content (ignoring
surrounding whitespace). A `FOLLOW` action is always considered valid.

The validator already knows how to:

- pull the full tweet body from the extended payload when a tweet is truncated,
- expand the shortened `t.co` links back to their original URLs using the
  tweet's URL entities, and
- HTML-decode the result before comparing.

Two common real-world cases are not handled today and cause legitimate shares to
be rejected (or to blow up):

1. **Attached media.** When a tweet has a photo or video, Twitter appends an
   extra `t.co` link to the tweet text pointing at the media. That link is not
   part of what the user typed, and it appears in the tweet's media entities
   (Twitter exposes these under both `entities.media` and
   `extended_entities.media`, and under the matching fields of the extended
   payload when the tweet is truncated). These media links must be removed from
   the text before the content comparison, so a share with an attached image
   still validates.

2. **Retweets.** When a user retweets the post rather than composing it, the
   event carries the original tweet under `retweeted_status` and the wrapper
   text is just the `RT @user: …` prefix (often truncated). In that case the
   original retweeted tweet is what should be validated — its full text, its URL
   expansion, and its media handling — not the wrapper.

Update the Twitter event validator so both cases work. Behavior to preserve and
pin down:

- A `FOLLOW` event validates to `true`.
- A `SHARE` event returns the cleaned, decoded tweet content (a string) when it
  matches the expected content after trimming, and `false` when it does not.
- The existing extended-payload selection, URL expansion, and HTML decoding keep
  working, including in combination with the two new cases above (e.g. a
  truncated retweet whose original carries shortened URLs and attached media).
- Comparison ignores only leading/trailing whitespace; the content otherwise
  must match.

The other social networks' validation behavior is unchanged.
