## Problem Statement

Hey, after I bumped Zope and the default response content type switched to text/plain, my MessageDialog popups are now totally broken — instead of the dialog I just see the raw HTML markup as plain text in the browser. Same thing happens when an error hits an exception view: I get the HTML error page dumped out as plain text instead of an actual rendered page. I checked and the Content-Type header on those responses is coming back as text/plain.

## Expected outcomes

- Message dialogs produced through `App.Dialogs.MessageDialog` should be served as HTML responses rather than as plain text.
- Message dialog content should still include the supplied title, message, and action when rendered.
- Exception views that do not set their own response content type should be served with an HTML content type.
- Exception views that already set a response content type should keep that existing content type instead of being overwritten.

## Implementation notes

The concrete implementation approach is up to you. Preserve existing public behavior outside the affected response content type handling, and avoid imposing unnecessary changes on unrelated dialog rendering or exception publishing paths.
