## Reading Stripe authorization for an event is broken

I'm wiring up Stripe payments through the Open Event API. POSTing my
stripe credentials for an event to `/v1/stripe-authorization` worked
fine and the record was created. Now my frontend needs to read those
settings back so I can show the connected account info on the
organizer dashboard.

Per the API docs the way to do that is:

```
GET /v1/events/<event_identifier>/stripe-authorization
Authorization: JWT <token>
Accept: application/vnd.api+json
```

I expected the response to be the stripe authorization payload
(stripe-email, stripe-publishable-key, etc.) that I created for this
event. Instead the request fails server-side and I don't get the data
back.

On the frontend I only ever have the event I'm working on — I don't
know the stripe-authorization's own id ahead of time, so going through
the event URL is the only practical way to look this up. Right now
that flow is broken.

It would also be good if the people who actually need this on the
dashboard — the event's organizers / co-organizers, i.e. the ones who
set up Stripe in the first place — could read it back themselves
instead of needing a higher-privileged account to fetch it for them.
