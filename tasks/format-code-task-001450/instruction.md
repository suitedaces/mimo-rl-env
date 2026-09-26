Terraform crash with 0.14.5 and sensitive variable - panic: value is marked, so must be unmarked first
### Terraform Version

```
Terraform v0.14.5
+ provider registry.terraform.io/iwarapter/pingfederate v0.0.8
```

### Terraform Configuration Files

```terraform
terraform {
  required_providers {
    pingfederate = {
      source  = "iwarapter/pingfederate"
      version = "0.0.8"
    }
  }
}

provider "pingfederate" {
  password = "2FederateM0re"
}

resource "pingfederate_notification_publisher" "mailserver" {
  name         = "demo"
  publisher_id = "demo"
  plugin_descriptor_ref {
    id = "com.pingidentity.email.SmtpNotificationPlugin"
  }

  configuration {
    fields {
      name  = "From Address"
      value = "someone@test.com"
    }
    fields {
      name  = "Email Server"
      value = "email-smtp.eu-west-1.amazonaws.com"
    }
    fields {
      name  = "SMTP Port"
      value = "25"
    }
    fields {
      name  = "Encryption Method"
      value = "SSL"
    }
    fields {
      name  = "SMTPS Port"
      value = "465"
    }
    fields {
      name  = "Verify Hostname"
      value = "false"
    }
    fields {
      name  = "Username"
      value = "someone"
    }
    sensitive_fields {
      name  = "Password"
      value = var.mail_server_password
    }
    fields {
      name  = "Test Address"
      value = "example@test.com"
    }
    fields {
      name  = "Connection Timeout"
      value = "30"
    }
    fields {
      name  = "Retry Attempt"
      value = "2"
    }
    fields {
      name  = "Retry Delay"
      value = "2"
    }
    fields {
      name  = "Enable SMTP Debugging Messages"
      value = "false"
    }
  }
}

variable "mail_server_password" {
  type      = string
  sensitive = true
}
```

### Debug Output
<!--
Full debug output can be obtained by running Terraform with the environment variable `TF_LOG=trace`. Please create a GitHub Gist containing the debug output. Please do _not_ paste the debug output in the issue, since debug output is long.

Debug output may contain sensitive information. Please review it before posting publicly, and if you are concerned feel free to encrypt the files using the HashiCorp security public key.
-->

### Crash Output

https://gist.github.com/iwarapter/3d151bcd232512e493c3d1851058bb60

### Expected Behavior

Apply succeeds as with tf-0.13.x

### Actual Behavior

 Panic Crash

### Steps to Reproduce

1. `terraform init`
2. `terraform apply`

### References

There have been a few other issues where this has presented - https://github.com/hashicorp/terraform/search?q=panic%3A+value+is+marked%2C+so+must+be+unmarked+first&type=issues however most say to upgrade to 0.14.(4/5)
