Missing labels from forced_response output
Hi,

I wrote a state-space system representation with labels, like:

``` Python
sys = ct.ss(
  A, B, C, D,
  name="motor",
  states=("Ia", "Wm"),
  inputs=("Va", "Tl"),
  outputs=("Ia", "Wm", "Va", "Tl"),
)
```

But after simulating it, the result (a `TimeResponseData`), lacks information about the labels of the simulated system:
``` Python
T = np.linspace(0, 0.360, 360)
Va = np.ones_like(T) * 36
Tl = np.linspace(0, 15, len(T))

res = ct.forced_response(motor, T, U=[Va, Tl], X0=[0, 0])
print(res.output_labels)  # this is None
print(res.input_labels)  # this is None
print(res.state_labels)  # this is None
```

I wanted to use `.to_pandas()`, and after assigning it manually, it works, so it's probably just a matter of passing it forward internally in the code:
``` Python
res.output_labels = motor.output_labels
res.input_labels = motor.input_labels
res.state_labels = motor.state_labels
df = res.to_pandas().set_index("time")
```

For completeness, this is the error if I try to use `.to_pandass()` without the abovementioned workaround:

``` Python
    648 # Create a dict for setting up the data frame
    649 data = {'time': self.time}
    650 data.update(
--> 651     {name: self.u[i] for i, name in enumerate(self.input_labels)})
    652 data.update(
    653     {name: self.y[i] for i, name in enumerate(self.output_labels)})
    654 data.update(
    655     {name: self.x[i] for i, name in enumerate(self.state_labels)})

TypeError: 'NoneType' object is not iterable
```

Thanks
