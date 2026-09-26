### snap login tests are unreliable on ppc64el / powerpc

When building and running the `cmd/snap` test suite on ppc64el (and also powerpc), the tests covering `snap login` are flaky / fail outright. On amd64 they pass.

Looking at how the login tests work, they spin up a pty via `/dev/ptmx` to feed a fake password into `terminal.ReadPassword`, because `requestLogin` reads the password directly from the terminal fd. That pty-based setup just doesn't behave consistently across architectures — what works on amd64 doesn't necessarily work on ppc64el/powerpc, and the test ends up either hanging or failing to deliver the input.

It would be much better if the login tests didn't depend on a real pty at all. The actual thing under test is the login flow logic (prompting for password, handling 2FA retry, trimming, etc.), not the terminal plumbing — so the password-reading step should be substitutable in tests without going through `/dev/ptmx`. That way the suite runs reliably on every architecture we care about.

I'd expect the swappable seam to look something like a package-level `ReadPassword` variable that tests can reassign to a fake.
