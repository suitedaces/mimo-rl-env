## ISSQN withholding invoice always uses the same partner regardless of city

We use `l10n_br_account_withholding` to automatically generate withholding invoices when confirming supplier invoices. This works fine for federal withholdings (IRRF, PIS, COFINS, CSLL) where the partner configured on the fiscal tax group is the right counterpart.

The problem is with **ISSQN**. ISSQN is a municipal tax, so the withholding invoice must be issued to the city hall (*Prefeitura*) of the municipality where the service was rendered — Prefeitura de São Paulo, Prefeitura do Rio de Janeiro, Prefeitura de Belo Horizonte, etc. Each one is a different legal entity (different CNPJ, different bank account, different journal in some setups).

### What we observe

When we confirm a purchase invoice that has an ISSQN withholding line, the generated WH invoice always has its `partner_id` taken from the partner configured on the fiscal tax group. That gives us a single hard-coded partner for *all* ISSQN withholdings, no matter which city the service line refers to.

So if we have a supplier invoice with services rendered in São Paulo and another with services rendered in Rio, both produce WH invoices pointing to the same Prefeitura — which is obviously wrong from an accounting/reporting standpoint, and we end up having to fix the partner manually on every single ISSQN WH invoice before posting it.

### What we expect

ISSQN withholding invoices should be addressed to the Prefeitura of the city indicated on the invoice line (the ISSQN city field already exists on the line). The setup should let us register, for each municipality where we operate, which `res.partner` represents that city's Prefeitura, so the module can pick the right one automatically when generating the WH invoice.

If for some reason no Prefeitura is registered for the city in question, falling back to the partner configured on the fiscal tax group is acceptable — that preserves today's behavior for users who haven't configured any city halls yet.

This should only kick in for taxes whose scope is municipal; federal/state withholdings should keep using the fiscal tax group's partner exactly as they do today.

I'd expect the way to mark a partner as a city hall to be a new boolean flag on `res.partner` (something like `wh_cityhall`), so we can search by `(city_id, wh_cityhall=True)` to find the right Prefeitura.
