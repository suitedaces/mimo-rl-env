## Can't close inactive or non-open channels from the app

I have a few channels in my wallet that I'd like to clean up:

- One of them shows as **inactive** — the remote peer has been offline for a while and isn't coming back.
- A couple are stuck in a non-open state (one pending, one that looks like it never made it past funding).

I went into the channel detail view for each of them and tapped **Close channel**, expecting the app to just take care of it. Instead it bounces me back to the channels list, the channel is still there, and I get a "Closing channel failed!" toast. Same thing happens for both the inactive one and the non-open ones.

The only channels I'm actually able to close from the UI are the ones that are currently open and active. For anything else, the close button is effectively a no-op — and those are exactly the channels I most want to get rid of, since they're just sitting there tying up funds.

It would be great if the **Close channel** button worked regardless of the channel's current state, so I can actually clean up channels with offline peers or ones that got stuck. Right now I have no way to do this from inside the app.
