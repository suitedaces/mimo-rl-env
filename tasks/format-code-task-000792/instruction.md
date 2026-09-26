## Problem Statement

Running a desec-stack instance and we've been getting hit by signup abuse pretty hard lately. The per-IP captcha throttle barely catches anything — someone just blasts through registrations from what looks like the same source by playing with headers, and we're also seeing waves of accounts all on the same email domain (like 30 fresh `@somedomain.tld` signups in a day) that nothing flags at all.

Separate thing while I'm here: `zone_exists()` in the pdns module is lying to us. We tried to create a zone, it said the zone already exists, but pdns actually returned a 422 saying it couldn't find the domain — so we end up bailing out on zones that aren't really there. Would be great if you could take a look at both.

## Expected outcomes

- Registration abuse protection should base per-source counting on the actual remote peer address seen by the application, so registrations from the same connection source cannot evade the captcha/lock flow by changing forwarding-related headers.
- Existing per-IP registration abuse behavior should remain configurable by limit and time window, and a registration that exceeds the configured recent-registration threshold for its remote source should enter the existing captcha/account-lock flow.
- Registration abuse protection should also consider the email hostname/domain portion of the submitted email address. When recent registrations for the same email hostname meet or exceed the configured limit within the configured window, the new registration should enter the existing captcha/account-lock flow, regardless of whether the remote IP differs.
- Registrations outside the relevant abuse-protection window should not by themselves cause a later registration to require captcha, and privacy cleanup should continue to clear stored registration IPs according to the active remote-IP abuse window.
- `desecapi.pdns.zone_exists(name)` should return `True` when the upstream PowerDNS API confirms that a zone exists, return `False` when the upstream response indicates that the domain could not be found, and raise an exception for other unexpected upstream responses instead of silently treating them as existing zones.

## Implementation notes

- The concrete data model queries, configuration plumbing, and validation locations are left to the implementer, as long as the observable registration, cleanup, and `zone_exists()` behavior above is satisfied.
- Do not rely on client-controlled forwarding headers for the registration abuse source key unless the application has independently established that such headers are trustworthy.
- Keep the behavior robust across different email local parts, domains, source addresses, and upstream PowerDNS error bodies; avoid solutions that only handle a single example value.

## Required upstream response literal (exact-match contract)

For `desecapi.pdns.zone_exists(name)`, an upstream PowerDNS HTTP 422 response whose body contains the literal `Could not find domain` MUST be treated as the domain-not-found case and return `False`. Other HTTP 422 bodies remain unexpected and MUST raise an exception.
