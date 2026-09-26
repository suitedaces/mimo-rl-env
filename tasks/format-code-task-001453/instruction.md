Upgrade to provider v1.44.0 breaks SignalR ID
### Community Note

* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* Please do not leave "+1" or "me too" comments, they generate extra noise for issue followers and do not help prioritize the request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment

<!--- Thank you for keeping this note for the community --->

### Terraform (and AzureRM Provider) Version

Terraform v0.12.20
+ provider.azurerm v1.44.0

### Affected Resource(s)

* `azurerm_signalr_service`

### Terraform Configuration Files

```hcl
resource "azurerm_signalr_service" "mysignalr01" {
  name                = "mysignalr01"
  location            = azurerm_resource_group.resource-group.location
  resource_group_name = azurerm_resource_group.resource-group.name

  sku {
    name     = "Standard_S1"
    capacity = 5
  }

  cors {
    allowed_origins = ["https://somewebsite.com"]
  }

  features {
    flag  = "ServiceMode"
    value = "Default"
  }

  features {
    flag  = "EnableConnectivityLogs"
    value = "True"
  }

  tags = {
    environment = azurerm_resource_group.resource-group.tags.environment
  }
}
```
### Expected Behavior

Terraform should not report any changes after upgrading from AzureRM 1.43.0 provider to AzureRM 1.44.0 

### Actual Behavior

Error: ID was missing the `signalR` element

It appears that casing was changed for ID from SignalR to signalR.
See documentation example for import:

terraform import azurerm_signalr_service.example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/terraform-signalr/providers/Microsoft.SignalRService/**SignalR**/tfex-signalr


### Steps to Reproduce

1. Upgrade AzureRM version from 1.43.0 to 1.44.0
2. Run `terraform plan`
