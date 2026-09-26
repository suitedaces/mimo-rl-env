## Front seat "Auto" heating triggers the wrong seat

I'm using the tesla_custom integration in Home Assistant. My car has the auto seat climate feature on the front seats, so the heated seat selects for `left` and `right` show an `Auto` option in addition to Off/Low/Medium/High.

When I pick any of Off/Low/Medium/High the seat heater behaves correctly — the left select controls the driver's seat, the right select controls the passenger's seat.

But as soon as I pick `Auto` from either of the front seat selects, the wrong seat reacts (or nothing visible happens on the seat I actually selected). Switching back to Low/Medium/High on that same select then works fine again, so the select itself is wired up to the right seat — it's specifically the `Auto` path that ends up targeting a different seat than the one I clicked.

Same thing happens in reverse: if `Auto` is currently active and I switch the select to one of the manual levels, the integration first tries to turn auto climate off, and that "off" call also seems to land on the wrong seat.

It looks like the regular seat heater command and the auto seat climate command don't agree on which seat index means "driver" vs "passenger", and the integration is feeding the same index to both. Could the Auto branch be fixed so that picking Auto on the left select actually turns on auto climate for the driver's seat (and right → passenger)?
