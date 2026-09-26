Argo CD's dex integration overwrites a custom dex.config.oauth2 yaml block
**Describe the bug**

When

**To Reproduce**

Deploy Argo CD with the following data for the `argo-cm` ConfigMap

```yaml
apiVersion: v1
data:
  application.instanceLabelKey: argocd.argoproj.io/instance
  dex.config: |
    oauth2:
      passwordConnector: ldap  # I want this enabled in dex to leverage the password grant type against LDAP
    connectors:
      - type: ldap
        name: LDAP
        id: ldap
        config:
          host: myldap.company.com
          usernamePrompt: Username
          userSearch:
            baseDN: "cn=users,dc=example,dc=com"
            username: uid
            idAttr: uid
            emailAttr: uid
            nameAttr: uid
          groupSearch:
            baseDN: "cn=groups,dc=freeipa,dc=example,dc=com"
            nameAttr: cn
  url: https://argocd.company.com/
kind: ConfigMap
```

When I examine generated dex config in the argocd-dex-server pod I find this

```yaml
# /shared/dex.yaml 
connectors:
- config:
    groupSearch:
      baseDN: cn=groups,dc=freeipa,dc=example,dc=com
      nameAttr: cn
    host: myldap.company.com
    userSearch:
      baseDN: cn=users,dc=example,dc=com
      emailAttr: uid
      idAttr: uid
      nameAttr: uid
      username: uid
    usernamePrompt: Username
  id: ldap
  name: LDAP
  type: ldap
grpc:
  addr: 0.0.0.0:5557
issuer: https://argocd.company.com//api/dex
oauth2:
  skipApprovalScreen: true  # passwordConnector was removed
staticClients:
- id: argo-cd
  name: Argo CD
  redirectURIs:
  - https://argocd.company.com/auth/callback
  secret: "<SOME SECRET VALUE HERE>"
- id: argo-cd-cli
  name: Argo CD CLI
  public: true
  redirectURIs:
  - http://localhost
  - http://localhost:8085/auth/callback
storage:
  type: memory
telemetry:
  http: 0.0.0.0:5558
web:
  http: 0.0.0.0:5556

```

I expected to see 

```yaml
oauth2:
   passwordConnector: ldap
   skipApprovalScreen: true
```
but instead I got:

```yaml
oauth2:
  skipApprovalScreen: true
```

**Expected behavior**

I want to be able to generate an oauth token with dex using the password grant-type when integrating with LDAP.  Therefore, when I pass in the following yaml to the argocd-cm ConfMap

```yaml
apiVersion: v1
data:
  application.instanceLabelKey: argocd.argoproj.io/instance
  dex.config: |
    oauth2:
      passwordConnector: ldap
      # Rest of the config....
```
argocd-dex will take that configuration into account when generating the dex configuration file.

**Version**

```shell
argocd: v2.1.2+7af9dfb
  BuildDate: 2021-09-02T18:05:23Z
  GitCommit: 7af9dfb3524c13e941ab604e36e49a617fe47d2e
  GitTreeState: clean
  GoVersion: go1.16.5
  Compiler: gc
  Platform: linux/amd64```
