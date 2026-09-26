## CORS AllowedOrigins doesn't support wildcard subdomains (e.g. `http://*.contoso.com`)

I'm using Azurite as a local emulator for Azure Storage during development. On our real storage account in Azure we have CORS rules configured for the Blob service that allow a wildcard subdomain pattern, something like:

```xml
<Cors>
    <CorsRule>
        <AllowedOrigins>http://*.contoso.com, http://www.fabrikam.com</AllowedOrigins>
        <AllowedMethods>PUT,GET</AllowedMethods>
        <AllowedHeaders>x-ms-meta-data*,x-ms-meta-target*,x-ms-meta-abc</AllowedHeaders>
        <ExposedHeaders>x-ms-meta-*</ExposedHeaders>
        <MaxAgeInSeconds>200</MaxAgeInSeconds>
    </CorsRule>
</Cors>
```

This is documented as supported by Azure Storage — see [Enabling CORS for Azure Storage](https://learn.microsoft.com/en-us/rest/api/storageservices/cross-origin-resource-sharing--cors--support-for-the-azure-storage-services#enabling-cors-for-azure-storage), which explicitly mentions that `*` can be used to allow any subdomain of a given domain.

When I push the same service properties (with the same CORS rules) into Azurite and then hit the blob endpoint from a page served at e.g. `http://app.contoso.com`, the browser's preflight request to Azurite fails and the request is rejected as a CORS violation. If I change AllowedOrigins to the exact origin `http://app.contoso.com` it works, and if I switch the endpoint back to the real Azure Storage account (same wildcard config), it also works.

So it looks like Azurite is treating the configured allowed origin as a literal string rather than honoring the `*` wildcard pattern that the Azure Storage service supports.

It would be great if Azurite's Blob CORS handling matched the real service here, so the same CORS configuration works against both Azurite and Azure Storage.
