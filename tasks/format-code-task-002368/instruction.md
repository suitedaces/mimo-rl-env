### PyBaMM Version

23,9

### Python Version

3.11

### Describe the bug

Sometimes experiement steps are skipped (e.g. skip a charge if you're already at that voltage). When this happens the solver returns an `EmptySolution`. The next step of the experiment then starts from the wrong point.

### Steps to Reproduce

```python3
import pybamm
import matplotlib.pyplot as plt

model = pybamm.lithium_ion.SPMe(
    {
        "SEI": "solvent-diffusion limited",
    }
)

exp = pybamm.Experiment(
    [(f"Rest for 24 hours (1 hour period)",)]
    + [
        (
            "Charge at C/3 until 4.1 V",
            "Hold at 4.1V until C/20",
            "Discharge at C/3 until 2.5 V",
        )
    ]
)

sim1 = pybamm.Simulation(model, experiment=exp)
sim1.solve(initial_soc=1)
sim2 = pybamm.Simulation(model, experiment=exp)
sim2.solve(initial_soc=0.9)

sols = [sim1.solution, sim2.solution]
labels = ["SOC=1", "SOC=0.9"]
fig, ax = plt.subplots(2, 2, figsize=(10, 4))
for sol, label in zip(sols, labels):
    ax[0,0].plot(sol["Time [h]"].data, sol["Terminal voltage [V]"].data, label=label)
    ax[0,1].plot(sol["Time [h]"].data, sol["X-averaged negative particle surface concentration [mol.m-3]"].data, label=label)
    ax[1,0].plot(sol["Time [h]"].data, sol["Total capacity lost to side reactions [A.h]"].data, label=label)
    ax[1,1].plot(sol["Time [h]"].data, sol["X-averaged negative total SEI thickness [m]"].data, label=label)
ax[0, 0].legend()

sim1.solution.cycles[1].steps
sim2.solution.cycles[1].steps
```

![image](https://github.com/pybamm-team/PyBaMM/assets/43040151/d3d0d3cf-9a58-4ee0-a69a-8df6e657ea00)



### Relevant log output

_No response_
