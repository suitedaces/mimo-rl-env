Namespace Selector Flag Based on Namespace Labels
### Is your feature request related to a problem? Please describe.

Our current kfo setup processes all namespaces in our kubernetes cluster because we are constantly adding/removing namespaces to/from our cluster. This causes issues as certain namespaces we don't want processed but we are unable to supply the operator with an explicit list of namespaces to process with the "--namespaces" flag due to the dynamic nature of our namespaces.

### Describe the solution you'd like

I would like a new flag named "--namespace-selector", or something similar, that takes in a string of format "labelKey1=labelValue1,labelKey2=labelValue2" and specifies which namespaces the operator should process based on the namespaces' labels. The use will be similar to the "--namespaces" flag, but instead of explicitly listing the names of namespaces to process, it gives the option to list  labels and process only namespaces that match all labels given.

### Describe alternatives you've considered

_No response_

### Additional context

_No response_
