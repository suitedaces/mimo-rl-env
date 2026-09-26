## OpenStack credential is missing a region field

I'm using AWX to run Ansible playbooks against an OpenStack cloud (OVH in my case). With OVH — and a few other providers — you have to tell the OpenStack SDK which region to talk to, otherwise authentication / API calls just don't go anywhere useful.

When I configure an "OpenStack" credential in AWX, the form lets me fill in:

- Username
- Password (API Key)
- Host (Authentication URL)
- Project (Tenant Name)
- Project (Domain Name)
- Domain Name
- Verify SSL

…but there's no field for the region. The `clouds.yaml` that AWX generates from this credential ends up looking like:

```yaml
clouds:
  devstack:
    auth:
      auth_url: ...
      username: ...
      password: ...
      project_name: ...
    verify: true
```

i.e. no `region_name` anywhere. For providers like OVH this isn't enough to actually use the cloud — the upstream `ansible-collections-openstack` inventory config (https://github.com/openstack/ansible-collections-openstack/blob/8255ec4c80f186aa7851f023b85007a593b6f42f/scripts/inventory/openstack.yml#L14) clearly expects region to be settable, and a plain `openstack.yaml` written by hand can include it just fine. AWX just doesn't expose it.

It would be great if the built-in OpenStack credential type had a region field so that:

1. Users can fill it in from the credential form in the UI.
2. When AWX renders the cloud config file used by the OpenStack modules / inventory, the region the user entered actually shows up there, so playbooks targeting OVH-style providers work without manual workarounds.

Leaving it empty should keep behaving like today (region simply not set), so existing OpenStack credentials that don't need a region aren't affected.

(For consistency with how other project-scoped fields are named on this credential, the new input id would be something like `project_region_name`.)
