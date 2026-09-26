# Problem Statement

I’m using `Force Invoiced` on a sales order, and the order header changes to `Invoiced`, but the order lines still show `To Invoice` in the lines/list views and reports. It makes filters based on sale order line invoice status look inconsistent, so I’m not sure if I’m missing a setting or if the force flag is only affecting the header.

# Expected Outcomes

- When `Force Invoiced` is enabled on a sales order, the invoice status shown for each of that order’s lines should also be `Invoiced`.
- Sale order line views, reports, and filters that rely on line invoice status should reflect the forced invoiced state consistently with the order header.
- When `Force Invoiced` is disabled again, sale order lines should no longer remain forced to `Invoiced`; their invoice status should return to the normal value computed by the existing business rules.
- The module usage documentation should make clear that enabling `Force Invoiced` affects both the sales order invoice status and the sale order line invoice status.

# Implementation Notes

- The exact model hooks, dependency declarations, and storage/update strategy are up to the implementer.
- Preserve the existing behavior for sales orders and sales order lines when `Force Invoiced` is not enabled.
- Keep documentation updates focused on the user-visible behavior rather than internal implementation details.
