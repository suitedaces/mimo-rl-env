## `observable login` doesn't tell the approval page which machine is asking

I work on a few different machines (personal laptop, work desktop, a small CI box) and I `observable login` from each of them as needed. The flow is fine — I run the command, get a confirmation code, open the auth page in the browser, and approve.

The problem is that the approval page in the browser only shows the confirmation code. There's nothing on it that identifies which machine actually kicked off the login. So when I'm staring at the page I can't tell "yes, this is the request I just made from my laptop" vs. some stale/other request — I'm essentially just trusting that the code matches and clicking through.

It would be a lot better if the CLI sent some kind of identifier for the device along with the auth request, so the approval page could show me "login request from <my-laptop>" next to the code. That way I can sanity-check that the request being approved is actually the one I just initiated, and over time I'd also have a clearer picture in the UI of which devices have asked for access.

I don't think the user should have to type anything in — the CLI knows what machine it's running on, it should just include that automatically when it kicks off the auth flow.

(I'm guessing the new field on the auth request body would be something like `deviceDescription`.)
