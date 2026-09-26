# Add a Phishing Army blocklist analyzer

We want IntelOwl to support reputation lookups against the public
[Phishing Army](https://phishing.army/) blocklist — a plain-text feed where each
line is a single blocked host (domain or IP), newline-separated.

Please add a new observable analyzer, exposed under the plugin name
`PhishingArmy`, that tells the user whether the observable they submitted is
present on that blocklist.

## Expected behavior

- The analyzer obtains the blocklist from the Phishing Army feed (a newline-
  separated list of hosts). It should fetch the feed when it doesn't already
  have a local copy of it; a cached copy may be reused.
- Running the analyzer returns a dictionary that contains a boolean entry under
  the key `found`. `found` is `True` when the observable is present on the
  blocklist and `False` otherwise.
- For `domain` and `ip` observables, the observable value is matched directly
  against the entries of the list (an entry counts as a match only when it
  equals the value, not when it merely appears as a substring of another entry).
- For `url` observables, only the URL's **hostname** is matched against the
  list — the scheme, path, query string, etc. must be ignored. A URL whose
  hostname is on the list is reported as found; a URL whose hostname is not on
  the list is reported as not found even if some other part of the URL happens
  to contain a blocked host.

The analyzer should fit naturally into the existing observable-analyzer
framework so that it is discoverable like the other analyzers and can be run
against a submitted observable.
