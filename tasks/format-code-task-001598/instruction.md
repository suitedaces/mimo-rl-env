## Stackdriver Context Graph adapter doesn't work with regional GKE clusters

I'm running Istio on a regional GKE cluster (location is something like `us-central1`) and using the Stackdriver Context Graph adapter from `mixer/adapter/stackdriver/contextgraph`. The workload entities reported by the adapter end up with a cluster container path that doesn't resolve to my actual GKE cluster — Context Graph can't tie the workloads back to the cluster resource.

It works fine when I switch to a zonal cluster (location like `us-central1-a`). Looking at the URLs the adapter generates for the cluster container under `container.googleapis.com`, the path it uses only matches the zonal cluster resource layout. GKE regional clusters live under a different path, so any cluster whose location is a region rather than a zone gets a broken/nonexistent container reference.

Could the contextgraph adapter detect whether `clusterLocation` refers to a region or a zone and emit the right resource path for each? Right now it's effectively zonal-only.
