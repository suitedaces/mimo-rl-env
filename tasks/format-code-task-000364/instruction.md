# Add ACH relationship and bank funding endpoints to BrokerClient

The Broker API lets you fund accounts. We support two of the funding building
blocks today only as raw HTTP — please add first-class support to `BrokerClient`
for **ACH relationships** and **recipient banks**, including the request/response
models and enums they need. Everything should be importable from the
`alpaca.broker` package the same way the existing models and enums are.

All of the new client methods accept `account_id` (and any other resource id) as
either a `UUID` or a `str`. An id that is not a valid UUID must raise
`ValueError` before any HTTP request is made.

## ACH relationships

Add these methods:

- `create_ach_relationship_for_account(account_id, ach_data)` — creates one ACH
  relationship by POSTing to `/accounts/{account_id}/ach_relationships`, and
  returns the created relationship as an `ACHRelationship`. There are two ways to
  create a relationship: by supplying raw bank/ACH details, or by supplying a
  Plaid processor token. `ach_data` must therefore be accepted as either of the
  two corresponding request models. If `ach_data` is neither, raise a
  `ValueError` and do not make any HTTP request.

- `get_ach_relationships_for_account(account_id, statuses=None)` — GETs
  `/accounts/{account_id}/ach_relationships` and returns a `List[ACHRelationship]`.
  `statuses` is an optional list of `ACHRelationshipStatus`; when provided and
  non-empty it must be sent as a single `statuses` query parameter whose value is
  the statuses joined with commas, preserving the given order. When omitted,
  `None`, or empty, no `statuses` query parameter is sent.

- `delete_ach_relationship_for_account(account_id, ach_relationship_id)` — DELETEs
  `/accounts/{account_id}/ach_relationships/{ach_relationship_id}`. It returns
  `None` on success.

### Request models

- `CreateACHRelationshipRequest` — for creating a relationship from raw ACH
  details, with fields: `account_owner_name` (str), `bank_account_type` (a
  `BankAccountType`), `bank_account_number` (str), `bank_routing_number` (str),
  and an optional `nickname` (str).
- `CreatePlaidRelationshipRequest` — for creating a relationship from a Plaid
  processor token, with a single `processor_token` (str) field.

### `ACHRelationship` model

Parses the API response into typed attributes, including at least: `id` (UUID),
`account_id` (UUID), `status` (an `ACHRelationshipStatus`), `account_owner_name`,
`bank_account_type` (a `BankAccountType`), `bank_account_number`, and
`bank_routing_number`.

## Recipient banks

Add these methods:

- `create_bank_for_account(account_id, bank_data)` — creates one bank by POSTing
  to `/accounts/{account_id}/recipient_banks` and returns the created `Bank`.
- `get_banks_for_account(account_id)` — GETs `/accounts/{account_id}/recipient_banks`
  and returns a `List[Bank]`.
- `delete_bank_for_account(account_id, bank_id)` — DELETEs
  `/accounts/{account_id}/recipient_banks/{bank_id}` and returns `None` on success.

### `CreateBankRequest` request model

Fields: `name` (str), `bank_code_type` (an `IdentifierType`), `bank_code` (str),
`account_number` (str), and the optional international-location fields `country`,
`state_province`, `postal_code`, `city`, and `street_address` (all str).

A bank is either **domestic** (identified by an ABA routing number) or
**international** (identified by a BIC). The location fields are meaningful only
for international banks. Enforce this at construction time:

- When `bank_code_type` is `IdentifierType.ABA`, none of the five location fields
  may be set; setting any of them raises `ValueError`.
- When `bank_code_type` is `IdentifierType.BIC`, all five location fields are
  required; leaving any of them unset raises `ValueError`.

### `Bank` model

Parses the API response into typed attributes, including at least: `id` (UUID),
`account_id` (UUID), `name`, `status` (a `BankStatus`), `account_number`,
`bank_code`, and `bank_code_type` (an `IdentifierType`).

## Enums

Add string enums (member name == wire value unless noted):

- `ACHRelationshipStatus`: `QUEUED`, `APPROVED`, `PENDING`.
- `BankAccountType`: `CHECKING`, `SAVINGS`.
- `IdentifierType`: `ABA`, `BIC`.
- `BankStatus`: `QUEUED`, `SENT_TO_CLEARING`, `APPROVED`, `CANCELED`.
