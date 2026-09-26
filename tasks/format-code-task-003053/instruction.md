## DEP enrollment form crashes when virtual server token is missing/expired

I was setting up a new DEP enrollment in the Zentral UI today. Filled out the
enrollment configuration as usual, hit Save, and instead of the enrollment
being created (or getting a nice validation error on the form), the request
blew up with a server error page.

After digging around with our ops team, it turned out the DEP virtual server
this enrollment was pointing at had an expired token — nobody had renewed it
in a while. So fair enough, the operation can't actually succeed. But from
the admin's perspective on the form page, the failure mode is pretty bad:

- I just see "Server Error" — no hint about *what* is wrong.
- I have no way to know from the UI that the problem is the token; I had
  to ask someone to look at the logs.
- Other failures coming from the DEP backend (e.g. when Apple's API is
  unhappy) get rendered as a normal form error on the page, so this case
  feels inconsistent.

I get the same crash if the virtual server has no token configured at all
(e.g. a freshly-created server that hasn't had its token uploaded yet) —
trying to use it from the enrollment form 500s instead of telling me to go
upload the token first.

It would be much nicer if these two situations (no token / expired token) were
surfaced on the enrollment form the same way other DEP backend errors are,
so the admin can read the message and go fix the token without needing log
access.
