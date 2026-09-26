Pulse builder equispace context doesn't work with multiple channels.
<!-- ⚠️ If you do not respect this template, your issue will be closed -->
<!-- ⚠️ Make sure to browse the opened and closed issues -->

### What is the current behavior?

Equispaced context of pulse builder doesn't work as expected. This is reported by @ajavadia .

### Steps to reproduce the problem

```python
with qk.pulse.build() as bgate_0_1:
    with qk.pulse.align_equispaced(duration=800):
        qk.pulse.play(qk.pulse.library.GaussianSquare(duration=600, amp=.5, sigma=30, width=400),
                      qk.pulse.DriveChannel(0))
        qk.pulse.play(qk.pulse.library.GaussianSquare(duration=300, amp=.5, sigma=30, width=100),
                      qk.pulse.DriveChannel(1))
```

returns

![image](https://user-images.githubusercontent.com/39517270/99616087-f542fd80-2a5f-11eb-8749-e1d7e63af13d.png)

We specified 800dt as the duration of context, however the total duration becomes 1100.
This is caused by following logic:

https://github.com/Qiskit/qiskit-terra/blob/bb627c62ddd54960a5e57a3cc73030d8071c7779/qiskit/pulse/transforms.py#L455-L467

`align_equispaced` relocates all sub schedule blocks (`_children`) with equispaced interval. In above example, the pulse on d0 and d1  (they are `Play` instruction schedule components) are independent children and will be aligned sequentially.

Interval is decided by (specified duration - current schedule duration) / (number of children), however if the schedule under the context consists of multiple channels, some schedules may be overlapped and net schedule duration may become shorter than the sum of all duration of children.

### What is the expected behavior?


### Suggested solutions

We should calculate the input schedule duration with
```
duration = sum([child_sched.duration for child_sched in schedule._children])
```
rather than
```
duration = schedule.duration
```

### Future extension
Above example intends to align two pulses at the center, thus we should use the context as follows:
```python
with qk.pulse.build() as bgate_0_1:
    with qk.pulse.align_equispaced(duration=800):
        qk.pulse.play(qk.pulse.library.GaussianSquare(duration=600, amp=.5, sigma=30, width=400),
                      qk.pulse.DriveChannel(0))
    with qk.pulse.align_equispaced(duration=800):
        qk.pulse.play(qk.pulse.library.GaussianSquare(duration=300, amp=.5, sigma=30, width=100),
                      qk.pulse.DriveChannel(1))
```
However this is not intuitive and we may be able to create `align_center` context to make multi-channel alignment easier.
```python
with qk.pulse.build() as bgate_0_1:
    with qk.pulse.align_center():
        qk.pulse.play(qk.pulse.library.GaussianSquare(duration=600, amp=.5, sigma=30, width=400),
                      qk.pulse.DriveChannel(0))
        qk.pulse.play(qk.pulse.library.GaussianSquare(duration=300, amp=.5, sigma=30, width=100),
                      qk.pulse.DriveChannel(1))
```

I'm bit busy recently so I hope someone in community will fix this...
