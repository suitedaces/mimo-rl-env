`value(expr, var_value)` works for affine expressions but not for variables or constraints

JuMP already provides a nice way to evaluate an affine expression under a user-supplied mapping from variables to numeric values:

```julia
value(a::GenericAffExpr, var_value::Function)
```

I find this very useful when I want to compute the primal value of things without going through an optimizer — e.g. plugging in a candidate solution coming from a heuristic, a warm-start, or some external computation, and seeing what each expression / constraint evaluates to.

The problem is that this only seems to work for `GenericAffExpr`. The same idea doesn't extend to a plain `VariableRef` or to a `ConstraintRef`:

```julia
model = Model()
@variable(model, x)
@variable(model, y)
@constraint(model, c, 2x + y <= 10)

assignment = Dict(x => 1.0, y => 2.0)
f = v -> assignment[v]

# works
value(2x + y, f)        # 4.0

# I'd like these to work too, but they don't
value(x, f)
value(c, f)
```

It would be very convenient if `value` accepted a `var_value::Function` for variables and constraints as well, so the same evaluation idiom works uniformly across expressions, variables, and constraints — without needing a model that has been solved.

Is there a reason this isn't supported, or could it be added?
