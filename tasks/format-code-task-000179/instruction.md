# Problem Statement

I’d like our sales quotations to pick a shipping method as soon as they’re created, instead of waiting until the order is confirmed or making the salesperson choose it manually. Ideally I could turn that on in Sales settings, and if the customer or delivery address changes on the quote, the carrier would refresh to match the new address.

# Expected outcomes

- A company-level Sales setting is available to enable or disable automatic carrier selection for newly created quotations. The setting is exposed through `res.config.settings.carrier_on_create` and stored on `res.company.carrier_on_create`.
- The new quotation-time setting is independent from the existing confirmation-time automatic carrier assignment setting: enabling or disabling one must not silently change the behavior controlled by the other.
- When quotation-time carrier selection is enabled and a new draft quotation is created without an already selected carrier, the quotation should automatically receive the carrier that matches the current customer or delivery address according to the existing delivery carrier rules.
- If a carrier has already been explicitly set on a newly created quotation, automatic quotation-time selection should not replace that existing carrier.
- When quotation-time carrier selection is disabled, creating a quotation should continue to leave carrier selection to the existing manual or confirmation-time flows.
- When the customer or delivery address is changed on a quotation while quotation-time carrier selection is enabled, the quotation’s selected carrier should refresh to match the new address.
- Confirming a sales order should continue to be governed by the existing confirmation-time automatic carrier assignment setting, independently of whether quotation-time carrier selection is enabled.

# Implementation notes

- Use the existing Odoo sales, delivery carrier, and configuration mechanisms where appropriate.
- The exact internal helper structure, validation location, and data flow are up to the implementer, provided the observable quotation creation, address-change, configuration, and confirmation behaviors above are satisfied.
- Keep compatibility with existing carrier assignment behavior outside the new quotation-time opt-in flow.
