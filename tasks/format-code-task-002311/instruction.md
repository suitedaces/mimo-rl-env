Prebid Server calls Cache unnecessarily
Right now, PBS sends a request to the Cache whenever `cache_markup` is true. If there are no bids, it still makes an _empty_ request to the Cache.

There's no value in this... it just hurts performance. We should avoid this call.
