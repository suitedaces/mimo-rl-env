`nikola init <sitename>` should produce an empty site by default

Right now when I run `nikola init mysite` I get a folder that's already filled with example posts, example stories and a gallery full of demo images. That's nice as a one-off "look what Nikola can do" preview, but it's a bit annoying as the default for someone who actually wants to start a real site — the first thing I have to do after `init` is go and delete all the sample content before I can start writing my own posts.

I'd expect `nikola init` to give me a clean scaffold by default (just the config plus the empty folder layout), and have the demo-content version be something I opt into explicitly when I want to look at the example site. There's already an `--empty` flag that does roughly the right thing for the clean case, so it feels like the defaults are just inverted from what most users probably want.

Could the defaults be flipped so that a plain `nikola init mysite` creates an empty site, and the example-filled site is opt-in via a flag? The docs and `CHANGES.txt` would need to be updated to match the new behaviour as well.

(Mentioned in #138.)

For the opt-in flag, something like `--demo` would be a natural name.
