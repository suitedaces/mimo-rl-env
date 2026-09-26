## Bot gets stuck retrying messages that violate the harmonization

I have a parser bot in my pipeline that occasionally receives messages where one of the fields contains a value that doesn't match the harmonization rules (e.g. something that should be an IP address but isn't, or an enum field with a value that's not in the allowed list).

When that happens, the bot doesn't move on. It logs the harmonization error, then retries the same message, logs the same error again, retries again, and so on — the pipeline effectively halts on that one bad message and just keeps spinning on it. The only way out is to stop the bot and manually remove the message from the queue.

That's not what I'd expect: if the value in the message is invalid according to the harmonization, retrying isn't going to make it valid. The bot should give up on that message immediately, dump it somewhere so I can look at it later, and continue processing the next message in the queue — same as it would for other "this message is broken, no point retrying" situations.

Could the harmonization-violation case be treated as a non-retryable error, with the offending message dumped for inspection instead of being retried indefinitely?
