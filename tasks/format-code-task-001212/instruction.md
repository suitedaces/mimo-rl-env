# Reserve raw materials when a Work Order is submitted

ERPNext already supports reserving stock against Sales Orders, but manufacturing has no
equivalent. When planners commit a Work Order they want its raw materials held back so other
transactions can't quietly consume the same on-hand stock. We want Work Orders to be able to
opt into reserving their raw materials.

Please add this capability with the following behavior:

- A Work Order gains an opt-in boolean field `reserve_stock` (label "Reserve Stock") that is
  **off by default**.

- Reservation only happens when stock reservation is enabled globally (the "Enable Stock
  Reservation" toggle in Stock Settings). If that setting is disabled, turning on
  `reserve_stock` must have no effect: the flag is cleared and nothing is reserved.

- When a Work Order with `reserve_stock` enabled is **submitted**, reserve its raw materials.
  For each required item that has a source warehouse and is a stock item, reserve as much of the
  required quantity as is currently *available to reserve* in that warehouse — i.e. the on-hand
  balance minus whatever is already reserved (by any voucher) in that warehouse. This produces a
  submitted Stock Reservation Entry against the Work Order, identified by voucher type
  `"Work Order"` and the Work Order's name as the voucher number, with the entry's reserved
  quantity equal to the amount actually reserved. A required item with nothing available to
  reserve gets no entry.

- Because reservations consume availability, a Work Order submitted later can only reserve what
  remains after earlier reservations against the same warehouse.

- The Work Order's `status` must reflect the outcome: `"Stock Reserved"` when every reservable
  required item is fully reserved, and `"Stock Partially Reserved"` when some but not all of the
  requirement could be reserved. (These are new status values.) If nothing was reserved, the
  status is unaffected by this feature.

- Cancelling a Work Order must release everything it reserved: all of its Stock Reservation
  Entries are cancelled, leaving no active reservation against the Work Order.

Keep the existing Sales Order stock-reservation behavior working unchanged.
