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

# Serieofarrays

```{raw-cell}
This notebook focuses on demonstrating how the classes :class:`fluiddyn.util.serieofarrays.SeriesOfArrays` can be used. 

This class can be used to create subsets from series of files. Let's first import it:
```

```{code-cell} ipython3
from fluiddyn.util.serieofarrays import SeriesOfArrays
```

This class works with a serie of files (or a file containing a serie of arrays) so we first need to create files. For this demo, we just create emtpy files.

```{code-cell} ipython3
import tempfile
from pathlib import Path
from shutil import rmtree
from pprint import pprint
```

```{code-cell} ipython3
path_dir = Path(tempfile.mkdtemp('_singleframe'))

for i0 in range(6):
    with open(path_dir / f'image{i0}.png', 'w') as f:
        pass
    
print([p.name for p in path_dir.rglob("*")])
```

We write a simple function to print the subsets of files that we are going to create...

```{code-cell} ipython3
def print_subsets(series):
    for serie in series:
        print('(', end='')
        for name in serie.iter_name_files():
            print(name, end=', ')
        print(')')
```

We show that we can create many different subsets quite easily:

```{code-cell} ipython3
series = SeriesOfArrays(path_dir / 'im*', 'i:i+2')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir / 'im*', 'i:i+2', ind_step=2)
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir / 'im*', 'i:i+3', ind_stop=3)
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir / 'im*', 'i:i+3:2')
print_subsets(series)
```

```{code-cell} ipython3
rmtree(path_dir, ignore_errors=True)
```

Let's consider another serie of files this time with two indices:

```{code-cell} ipython3
path_dir = Path(tempfile.mkdtemp('_doubleframe'))

for i0 in range(3):
    with open(path_dir / f'im_{i0}a.png', 'w') as f:
        pass
    with open(path_dir / f'im_{i0}b.png', 'w') as f:
        pass
    
print([p.name for p in path_dir.rglob("*")])
```

Creating subsets of files is still very simple:

```{code-cell} ipython3
series = SeriesOfArrays(path_dir / 'im*', 'i, 0:2')
print_subsets(series)
```

```{code-cell} ipython3
series = SeriesOfArrays(path_dir / 'im*', '0:2, i')
print_subsets(series)
```

Of course we can do many more things with these objects:

```{code-cell} ipython3
pprint([name for name in dir(series) if not name.startswith('__')])
```

```{code-cell} ipython3
pprint([name for name in dir(series.serie) if not name.startswith('__')])
```

```{code-cell} ipython3
rmtree(path_dir, ignore_errors=True)
```

```{raw-cell}
For the documentation on these methods, see the presentation of the API of the module :mod:`fluiddyn.util.serieofarrays`.
```
