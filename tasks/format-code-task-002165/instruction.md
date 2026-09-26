## Bug Report

**What did you do?**

I have a CR yaml that contains camelCase key names. When the ansible playbook is called, all keys are converted to snake_case.

**What did you expect to see?**

I expect all variable key names for all CR settings to retain the exact spelling. I do not expect them to be converted to snake_case if they are camelCase.

**What did you see instead? Under which circumstances?**

All camelCase key names are converted to snake_case.

**Environment**
* operator-sdk version: 0.9.0

* Kubernetes version information:

```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.2", GitCommit:"66049e3b21efe110454d67df4fa62b08ea79a19b", GitTreeState:"clean", BuildDate:"2019-05-16T16:23:09Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"13+", GitVersion:"v1.13.4+6569b4f", GitCommit:"6569b4f", GitTreeState:"clean", BuildDate:"2019-07-10T19:31:33Z", GoVersion:"go1.11.6", Compiler:"gc", Platform:"linux/amd64"}
```
* Kubernetes cluster kind:

OpenShift 4.1

* Are you writing your operator in ansible, helm, or go?

Ansible

**Possible Solution**

*shrug*

**Additional context**

Create a CR with this in the spec:

```
  deployment:
    version: "1.0"
    affinity:
      pod:
        preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchExpressions:
              - key: security
                operator: In
                values:
                - S2
            topologyKey: failure-domain.beta.kubernetes.io/zone
```

Now have the ansible script look at the deployment dict - e.g. print it out in a debug msg:

```
- debug:
    msg: "STARTING OPTEST: deployment is: {{ deployment }}"
```

Notice all the camelCase keys are converted to snake_case:

```
    "msg": "STARTING OPTEST: deployment is: {u'version': u'1.0', u'affinity': {u'pod': {u'preferred_during_scheduling_ignored_during_execution': [{u'pod_affinity_term': {u'label_selector': {u'match_expressions': [{u'operator': u'In', u'values': [u'S2'], u'key': u'security'}]}, u'topology_key': u'failure-domain.beta.kubernetes.io/zone'}, u'weight': 100}]}}}"
}
```

**Replication Procedures**

ATTACHMENT: [optest.zip](https://github.com/operator-framework/operator-sdk/files/3463245/optest.zip)

I have attached a .zip file containing a very simple/small test operator. It shows this problem. Here is how I tested. I am running with a CRC VM running OpenShift 4.1.6 - you will notice the push-operator.sh script will push to the CRC image registry. If you run this test, you will probably need to change push-operator.sh to push to your own registry and make sure you change `deploy/operator.yaml` so the image references pull from your registry.

The steps are as follows - I assume the cwd is in the optest directory after you unzip the attachment.

1. `./build-operator.sh` -- this builds the operator image
2. `./push-operator.sh` -- this pushes the operator image to an image registry in CRC VM
3. `./create-operator.sh` -- this creates the operator resources in the cluster
4. `oc get deployment optest -n optestns` -- run this to confirm the operator is up and running
5. `./create-cr.sh` -- create the CR which contains camelCase key names 
6. `oc logs deployment/optest -n optestns -c ansible` -- after the operator runs, get its logs to see the camelCase has been converted to snake_case.

The operator's playbook has only a 2-line role that looks like this (see `roles/optest/tasks/main.yml`):

```
- debug:
    msg: "STARTING OPTEST: deployment is: {{ deployment }}"
```

When step 5 above creates a CR that looks like this (see `deploy/crds/optest_v1alpha1_optest_cr.yaml`):

```
apiVersion: optest.example.com/v1alpha1
kind: Optest
metadata:
  name: example-optest
spec:
  deployment:
    version: "1.0"
    affinity:
      pod:
        preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchExpressions:
              - key: security
                operator: In
                values:
                - S2
            topologyKey: failure-domain.beta.kubernetes.io/zone
```

The playbook outputs the following in the logs - which you see when running step 6:

```
$ oc logs deployment/optest -n optestns -c ansible
Setting up watches.  Beware: since -r was given, this may take a while!
Watches established.
/tmp/ansible-operator/runner/optest.example.com/v1alpha1/Optest/optestns/example-optest/artifacts/5679351375816964720//stdout
ansible-playbook 2.7.10
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/usr/share/ansible/openshift']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 2.7.5 (default, Oct 30 2018, 23:45:53) [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
Using /etc/ansible/ansible.cfg as config file

/tmp/ansible-operator/runner/optest.example.com/v1alpha1/Optest/optestns/example-optest/inventory/hosts did not meet host_list requirements, check plugin documentation if this is unexpected
/tmp/ansible-operator/runner/optest.example.com/v1alpha1/Optest/optestns/example-optest/inventory/hosts did not meet script requirements, check plugin documentation if this is unexpected

/tmp/ansible-operator/runner/optest.example.com/v1alpha1/Optest/optestns/example-optest/inventory/hosts did not meet script requirements, check plugin documentation if this is unexpected

PLAYBOOK: 5f13ba22c7b749339cd785f127d423d1 *************************************
1 plays in /tmp/ansible-operator/runner/optest.example.com/v1alpha1/Optest/optestns/example-optest/project/5f13ba22c7b749339cd785f127d423d1

PLAY [localhost] ***************************************************************

TASK [Gathering Facts] *********************************************************


ok: [localhost]
META: ran handlers

TASK [optest : debug] **********************************************************
task path: /opt/ansible/roles/optest/tasks/main.yml:1
ok: [localhost] => {
    "msg": "STARTING OPTEST: deployment is: {u'version': u'1.0', u'affinity': {u'pod': {u'preferred_during_scheduling_ignored_during_execution': [{u'pod_affinity_term': {u'label_selector': {u'match_expressions': [{u'operator': u'In', u'values': [u'S2'], u'key': u'security'}]}, u'topology_key': u'failure-domain.beta.kubernetes.io/zone'}, u'weight': 100}]}}}"
}
META: ran handlers
META: ran handlers

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0   
```

Notice the `deployment` dict now has keys like `preferred_during_scheduling_ignored_during_execution` and `pod_affinity_term` when they are really camelCase in the CR such as `preferredDuringSchedulingIgnoredDuringExecution` and `podAffinityTerm`

It would be reasonable to expose this as a per-watch option in `watches.yaml`, e.g. something like a `snakeCaseParameters` toggle (defaulting to the current behavior to stay backwards compatible).
