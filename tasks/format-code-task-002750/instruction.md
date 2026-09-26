## `Manager.Reset` fails on HPE iLO4 (gen9) when the manager doesn't advertise `ResetType@Redfish.AllowableValues`

I'm using gofish to reset the BMC on an HPE Gen9 server (iLO4). The Actions block returned by the manager looks like this — note there's only a `target`, no `ResetType@Redfish.AllowableValues`:

```json
"Actions": {
    "#Manager.Reset": {
        "target": "/redfish/v1/Managers/1/Actions/Manager.Reset/"
    }
}
```

So `SupportedResetTypes` ends up empty on the parsed `Manager`. When I call `manager.Reset(...)`, the server rejects the request with `Base.0.10.ActionNotSupported` and the BMC is not reset. Sniffing the request shows gofish posts a body of `{"Action":"Manager.Reset"}`, which iLO4 doesn't accept.

Per the [Manager schema](https://redfish.dmtf.org/schemas/v1/Manager.v1_18_0.yaml), `ResetType` on the reset request body is described as:

> This parameter shall contain the type of reset. The service can accept a request without the parameter and perform an implementation specific default reset. Services should include the @Redfish.AllowableValues annotation for this parameter to ensure compatibility with clients, even when ActionInfo has been implemented.

So when a manager doesn't advertise any allowable reset types, the spec-compliant thing is to send the request without a `ResetType` and let the service do its default reset. I confirmed on iLO4 that posting an empty body to the reset target works and the BMC reboots as expected.

Could `manager.Reset` handle this case so it works against managers (like HPE Gen9 / iLO4) that don't expose `ResetType@Redfish.AllowableValues`?
