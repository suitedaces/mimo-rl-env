## Kubeapps fails to sync AppRepositories on Kubernetes 1.20

I tried installing the latest Kubeapps on a Kubernetes 1.20 cluster (still a supported upstream version) and the apprepository-controller can't get the bundled `bitnami` repo to sync. New AppRepositories I add through the dashboard show the same problem — they never finish syncing and no charts ever appear.

Looking at the controller pod, it errors out whenever it tries to reconcile an AppRepository. The Job that does the actual chart fetch never gets created because the periodic sync resource the controller wants to create on my behalf isn't something my 1.20 API server accepts under the group/version the controller is asking for.

Steps:

1. `kind create cluster` (or any other k8s 1.20 cluster)
2. Install Kubeapps from the chart
3. Wait for the default `bitnami` AppRepository to sync — it never does
4. `kubectl logs -n kubeapps deploy/kubeapps-internal-apprepository-controller` shows reconcile errors and no sync resource is ever created in the kubeapps namespace

The previous release worked fine on the same cluster, so something between then and now made the controller incompatible with 1.20. It would be good to keep Kubeapps working on 1.20 — it's not that old and it's still in support upstream.
