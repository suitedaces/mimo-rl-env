## Support Managed Identity auth for the azure-arm builder

I'd like to run Packer with the `azure-arm` builder from inside an Azure VM that has a system-assigned managed identity, and have Packer use that identity to talk to Azure — without me having to hand it a service principal.

### What I'm trying to do

I provisioned a small Azure VM to run my Packer builds on. The VM has managed identity enabled and the identity has been granted the right roles on my subscription. Tools like `az` already pick this up automatically on that VM — I never have to put credentials in any config.

I'd like Packer to do the same thing. My intent is to leave `client_id`, `client_secret` (and ideally `subscription_id`) out of my packer template entirely, since the VM Packer is running on already has an identity that can do the work. That way I don't have to create a separate service principal just for Packer, and I don't have to ship a `client_secret` around in my templates / repos.

### What actually happens

If I drop those fields from the azure-arm builder config, the build never even starts — config validation rejects the template up front because `client_id`, `client_secret` and `subscription_id` are treated as unconditionally required.

So today there's basically no way to use the azure-arm builder without supplying a full service-principal-style credential set, even when Packer is running somewhere that already has an Azure identity attached to it.

### What I'd like

When Packer is running on an Azure VM that has a managed identity, the azure-arm builder should be able to use that identity to authenticate to Azure ARM instead of requiring a service principal in the template. Concretely, it should be possible to leave the SPN-style fields out of the builder config and have the build still run (using the host VM's identity), the same way the device-login path today doesn't require `client_id`/`client_secret`.

This would make Packer much nicer to use as part of an Azure-native CI/CD setup.
