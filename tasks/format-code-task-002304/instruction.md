## Dmark USSD transport sends non-empty `content` on the first message of a new session

I'm building a USSD menu application on top of Vumi and using the Dmark USSD transport to handle inbound traffic. My application worker reacts to inbound messages and uses `session_event` plus `content` to drive the menu state machine — on `SESSION_NEW` I show the root menu (no input expected yet), and on `SESSION_RESUME` I treat `content` as the user's menu selection.

The problem: when a user dials our short code, the very first inbound message the application receives has `session_event == SESSION_NEW` as expected, **but `content` is also populated** — it contains whatever was in the `ussdRequestString` query param on the initial Dmark request. So my menu code immediately sees a "user input" on the session-establishment message and tries to interpret it as a menu choice, before the user has actually had a chance to type anything. The whole menu gets pushed one step ahead.

I checked how the other USSD transports in Vumi behave for comparison, and the convention seems to be: the `SESSION_NEW` message carries no content (it just signals "a session has been established"), and the user's actual input only starts arriving on subsequent `SESSION_RESUME` messages. The Dmark transport doesn't follow that convention — it just forwards `ussdRequestString` verbatim on every request regardless of whether the session is new or resuming.

I think the Dmark transport should match the other USSD transports here: on the first request of a session (`SESSION_NEW`), the published message's `content` should reflect that there's no user input yet, and only resumed-session messages should carry the value from `ussdRequestString`. Otherwise every Vumi USSD app has to special-case Dmark.
