# Manage custom nameservers for a registered DNS domain

Our users register DNS domains through IBM Cloud (SoftLayer) and frequently need to point a
registered domain at a custom set of nameservers from Terraform. Today the provider has no way to
discover a domain registration or to manage its nameservers. Add that capability.

## Data source: `ibm_dns_domain_registration`

Looks up a domain registration by its name.

- Input argument `name` (string, **required**): the registered domain name to look up.
- Exported attribute `name_servers` (**computed**): the list of nameserver hostnames currently
  configured on the registration, as strings.

## Resource: `ibm_dns_domain_registration_nameservers`

Manages the custom nameservers of an existing domain registration.

- Argument `dns_registration_id` (string, **required**): the identifier of the domain registration
  to manage.
- Argument `name_servers` (**required**): the desired collection of nameserver hostnames (strings)
  the registration should use.
- Exported attribute `original_name_servers` (**computed**): the nameservers that were present
  before this resource took over management, so they can be restored later.

## Nameserver validation

Every value supplied in `name_servers` must be a syntactically valid DNS hostname. Validation must
happen during configuration validation (i.e. before any API call is made), so that an invalid
value causes a validation error rather than being sent to the backend. A value is valid only if all
of the following hold:

- it is non-empty and at most 253 characters long;
- it consists of dot-separated labels and contains at least one dot (at least two labels);
- every label is between 1 and 63 characters long;
- every label contains only ASCII letters, digits, and hyphens; and
- no label begins or ends with a hyphen.

Any value that violates one or more of these rules must produce a validation error for the
`name_servers` argument; values that satisfy all of them must validate cleanly.

The provider must continue to pass its internal schema validation with these additions in place.
