This seems to be due to a bug in how we are interfacing with autograd, or -- less likely -- a bug in autograd itself.

If the user provides a quantum function `func` with multiple input arguments in its signature, we can only successfully call `qml.jacobian(func, argnum=0)`, `qml.jacobian(func, argnum=1)`, etc., but not `qml.jacobian(func, argnum=[0,1])` (raises some error inside autograd). 

Since we've coded `jacobian` to behave nicely if all the arguments are combined into an array, a suitable alternate usage is available. Would be nice to figure this bug out at some stage
