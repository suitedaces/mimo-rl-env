## `Queue::createPayloadUsing` callbacks overwrite each other

I'm using `Queue::createPayloadUsing` (added in 5.7.7) in my `AppServiceProvider` to attach some extra fields onto every queued job payload — works great on its own.

This week I installed Laravel Telescope (beta), and after that my own payload fields stopped showing up on queued jobs. Digging in, it looks like Telescope also registers a callback via `Queue::createPayloadUsing`, and whichever side calls it last wins — the other one is silently dropped.

So today it's effectively "only one consumer of this hook in the entire app." That seems unfortunate, because the hook is exactly the kind of thing multiple unrelated packages (Telescope, my app, future first-party stuff that wants to share data across queues) will reasonably want to use at the same time.

Could `createPayloadUsing` support being called more than once, with all registered callbacks contributing to the final payload? Single-callback usage should keep behaving the same as it does today so existing apps don't break.
