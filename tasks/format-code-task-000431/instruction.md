Solr has a feature that gives an HTTP endpoint to ask Solr Nodes to gracefully terminate.

Kuberentes has container lifecycle hooks that allow for post-start and pre-stop actions: https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers

We should explicitly use the ./solr stop -p <solr_port> option in Solr and call this as a pre-stop action. That way Solr can determine how to best stop itself, until a timeout is reached and kubernetes stops the process itself.

There are some niceties given for stopping in docker-solr, but I'm not sure how much we want to dedicate ourselves to this image of Solr. Something to think about.
