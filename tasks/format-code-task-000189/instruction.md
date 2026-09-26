## BroydenSolver behaves inconsistently with other nonlinear solvers (label + recording)

I'm running a model where I'm experimenting with different nonlinear solvers
(BroydenSolver vs NewtonSolver vs NonlinearBlockGS) on the same group, and
I have a case recorder attached so I can compare their iteration behavior
side-by-side. While doing this I noticed two ways in which BroydenSolver
sticks out from the others — both feel unintentional:

**1. Solver label doesn't follow the same naming convention**

When I look at the solver name in printed output / recorded metadata, the
other nonlinear solvers I'm using are labeled with the `NL:` prefix
(`NL: Newton`, `NL: NLBGS`, etc.), but Broyden just shows up as `BROYDEN`
— no prefix. Looks like a missed alignment with the rest of the
nonlinear-solver family.

**2. Extra cases recorded per Broyden iteration**

With the same recorder config attached, I get noticeably more recorded
entries from BroydenSolver per outer iteration than I do from the other
nonlinear solvers in the same setup. Switching the solver from Newton to
Broyden on the same group, the number of cases I get back from the recorder
goes up even though the iteration count itself didn't. It looks like Broyden
is producing an extra layer of recording during its iteration that the other
nonlinear solvers don't, which inflates the case list and makes it
inconsistent to compare runs across solvers.

I'd expect BroydenSolver to label itself the same way the rest of the
nonlinear solvers do, and to record at the same granularity as them so that
swapping solvers doesn't change how the recorder sees the run.
