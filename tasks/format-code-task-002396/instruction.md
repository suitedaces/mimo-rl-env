## Email block list bypassed by subdomains and uppercase

Follow-up to #15672.

After adding a domain to `ProhibitedEmailDomain` (and similarly for entries already in `disposable_email_domains.blocklist`), I'm still seeing signups go through that obviously should have been blocked. Two patterns in particular:

1. **Subdomains.** I block `spam-example.com`, but registrations with addresses like `someone@mail.spam-example.com` or `someone@smtp.spam-example.com` are accepted.
2. **Case.** Addresses with the domain in mixed case, e.g. `someone@Spam-Example.com` or `someone@SPAM-EXAMPLE.COM`, are also accepted.

Looking at the registration form's email validation, the prohibited-domain check compares the part after `@` to the block list as-is. So anything that isn't a byte-for-byte lowercase match of the exact domain I entered slips through, which makes the block list pretty easy to evade — a spammer just has to point a subdomain at the same MX, or send the form with a different capitalization.

When I add a domain to the block list, I'd expect any email whose address is hosted on that domain — including its subdomains, and regardless of how the user capitalized it in the form — to be rejected on signup.
