---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Demo `SerieOfArrays`

+++

This notebook focuses on demonstrating how the classes {class}`fluiddyn.util.serieofarrays.SeriesOfArrays` can be used.
This class can be used to create subsets from series of files. Let's first import it:

```{code-cell} ipython3
from fluiddyn.util.serieofarrays import SeriesOfArrays
```

This class works with a serie of files (or a file containing a serie of arrays) so we first need to create files. For this demo, we just create emtpy files.

```{code-cell} ipython3
import tempfile
from pathlib import Path
from pprint import pprint
from shutil import rmtree
```

```{code-cell} ipython3
path_dir = Path(tempfile.mkdtemp('_singleframe'))

for i0 in range(6):
    with open(path_dir / f'image{i0}.png', 'w'):
        pass

print(sorted(p.name for p in path_dir.rglob("*")))
```

We write a simple function to print the subsets of files that we are going to create...

```{code-cell} ipython3
def print_subsets(series):
    print(series)
    for serie in series:
        print(serie.get_name_arrays())
```

We show that we can create many different subsets quite easily:

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'i:i+2')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'i:i+2', ind_step=2)
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'i:i+3', ind_stop=3)
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'i:i+3:2')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'pairs')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'all1by1')
print_subsets(series)
```

```{code-cell} ipython3
rmtree(path_dir, ignore_errors=True)
```

Let's consider another serie of files this time with two indices:

```{code-cell} ipython3
path_dir = Path(tempfile.mkdtemp('_doubleframe'))

for i0 in range(3):
    for letter in "ab":
        with open(path_dir / f'im_{i0}{letter}.png', 'w'):
            pass

print(sorted(p.name for p in path_dir.rglob("*")))
```

Creating subsets of files is still very simple:

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'i, 0:2')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, '0:2, i')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'pairs')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir, 'all1by1')
print_subsets(series)
```

Of course we can do many more things with these objects:

```{code-cell} ipython3
pprint([name for name in dir(series) if not name.startswith('__')])
```

Internally, {class}`fluiddyn.util.serieofarrays.SeriesOfArrays` uses an instance
(its attribute `serie`) of the class {class}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles`.

```{code-cell} ipython3
pprint([name for name in dir(series.serie) if not name.startswith('_') and not "index_slices" in name])
```

```{code-cell} ipython3
rmtree(path_dir, ignore_errors=True)
```

```{raw-cell}
See also the presentation of the API of the module :mod:`fluiddyn.util.serieofarrays`.
```
