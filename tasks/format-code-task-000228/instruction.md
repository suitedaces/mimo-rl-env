### What is the expected enhancement?

As pointed out by @maddy-tod in #3288 :

>  ... it might be good to have this as a function on the gate for example Gate.is_parameterized() just for clarity. This could potentially introduce confusion for gates that are not able to be parameterized though.

There are a few places in the code which handle parameterized gates differently from fully bound gates, e.g. `Optimize1qGates`, `CommutationAnalysis`, `Collect2qBlocks`, and the unroller . Rather than having each `any(isinstance(param, ParameterExpression) for param in op.params)`, it might be helpful to have a `.is_parameterized` method on the base `Instruction` class.

Questions:
- What is a returned for a gate that accepts no `params`?
- Do we distinguish between unbound (`ParameterExpression(θ)`) and bound (`ParameterExpression(3.25)`) parameters?
