ACL CLI does not validate policy rules when creating a new policy
### Nomad version
Nomad v0.7.0-dev 

### Issue
A policy of the following syntax: 

```
{                                               
    "Name": "my-policy",                        
    "Description": "This is a great policy",    
    "Rules": "anything"                           
}                                                                                            
```
Can be successfully created via the `nomad acl policy apply` command.
