---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Timer

```{raw-cell}
This notebook demonstrates how the classes :class:`fluiddyn.util.timer.Timer` and :class:`fluiddyn.util.timer.TimerIrregular` can be used to loop with controled times.

We import the 2 classes:
```

```{code-cell} ipython3
from fluiddyn.util.timer import Timer, TimerIrregular
```

Let's first use the regular timer:

```{code-cell} ipython3
timer = Timer(0.02)

for i in range(10):
    print(f'before tick {i}... ', end='')
    timer.wait_tick()
    print("It's time to tick", i)
```

Ok. This is the simplest way to use it. But we don't see when the timer ticked. Let's print these times:

```{code-cell} ipython3
timer = Timer(0.02)

for i in range(10):
    print(f'before tick {i}... ', end='')
    t_tick = timer.wait_tick()
    print("It's time to tick", i, f'(t = {t_tick:.4f} s)')
```

Now, we see that it's ticking regularly... and it seems with a quite good accuracy for many needs.

But what can we do if we need irregular steps between the ticks?

```{code-cell} ipython3
times = [0, 0.05, 0.07, 0.1]
timer = TimerIrregular(times)

for i in range(len(times)-1):
    print(f'before tick {i}... ', end='')
    t_tick = timer.wait_tick()
    print("It's time to tick", i, f'(t = {t_tick:.4f} s)')
```
