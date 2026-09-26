I'm having a problem getting the iam roles to match when the assumed role contains a path.

```
kubeconfig settings:
apiVersion: v1
clusters:
- cluster:
    server: <endpoint>
    certificate-authority-data: <cert>
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: aws
  name: aws
current-context: aws
kind: Config
preferences: {}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      command: heptio-authenticator-aws
      args:
        - "token"
        - "-i"
        - "eks-cluster"
        - "auth-test"
        - "-r"
        - "arn:aws:iam::000000000000:role/roles/SomeRole"

```
Non Working ConfigMap:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::000000000000:role/worker-node
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
    - rolearn: arn:aws:iam::000000000000:role/roles/SomeRole
      username: admin:{{SessionName}}
      groups:
        - system:masters
```

Working ConfigMap:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::000000000000:role/worker-node
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
    - rolearn: arn:aws:iam::000000000000:role/SomeRole
      username: admin:{{SessionName}}
      groups:
        - system:masters
```

As you can see from the non-working and working comparison I have to trim out the iam path to get the authentication to work.  (arn:aws:iam::000000000000:role/roles/SomeRole vs  arn:aws:iam::000000000000:role/SomeRole) Technically on AWS side the arn with the trimmed path is not the same role.
