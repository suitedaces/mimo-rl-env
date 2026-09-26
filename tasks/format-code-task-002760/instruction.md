Allow specifying timestamp in webhook event signature verification
### Is your feature request related to a problem? Please describe.

I am using the Stripe node API in a setting in which inbound events are placed in a queue before being processed by my code. As a result, there is a variable delay between when the webhook event is sent by Stripe and when it reaches my code. The only way to deal with this right now is to either increase tolerance in the call to `constructEvent` or to implement my own verification. 

### Describe the solution you'd like

I would prefer if `constructEvent` had an optional parameter that is the timestamp against which the webhook event timestamp will be compared. (Currently it always uses `now()` for comparison.) This would allow me to pass in the timestamp of when my queueing system received the message (rather than the time when I am processing the message). 


### Describe alternatives you've considered

Writing my own signature verification

### Additional context

_No response_
