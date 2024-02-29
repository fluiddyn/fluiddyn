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

# Paramcontainer

```{raw-cell}
This notebook shows how the class :class:`fluiddyn.util.paramcontainer.ParamContainer` can be used. 
```

```{code-cell} ipython3
from fluiddyn.util.paramcontainer import ParamContainer
```

Let's consider code taken from fluidimage. The object containing the parameter is initialized in the package. It is first created empty:

```{code-cell} ipython3
params = ParamContainer(tag='params')
```

We then fill it with default parameters:

```{code-cell} ipython3
# taken from fluidimage.work.piv.singlepass
params._set_child('piv0', attribs={
        'shape_crop_im0': 48,
        'shape_crop_im1': None,
        'displacement_max': None})

params.piv0._set_doc("""Parameters describing one PIV step.""")

params.piv0._set_child('grid', attribs={
    'overlap': 0.5,
    'from': 'overlap'})

params.piv0.grid._set_doc("""
Parameters describing the grid.

overlap : float (0.5)
    Number smaller than 1 defining the overlap between interrogation windows.

from : str {'overlap'}
    Keyword for the method from which is computed the grid.
""")
```

There are other functions to add attribute to a child:

```{code-cell} ipython3
params.piv0._set_attrib
params.piv0._set_attribs
```

The ParamContainer object can be used in the code to generate the documentation, as for example in this [page](http://fluidimage.readthedocs.io/en/latest/generated/fluidimage.topologies.piv.html).

+++

Then the user has to modify the default parameters in a python script. She/he can first create the object in ipython and play with it. The representation of the object shows the parameters and their values:

```{code-cell} ipython3
params.piv0
```

It is also easy to print the documentation (or part of the documentation):

```{code-cell} ipython3
params.piv0._print_doc()
```

```{code-cell} ipython3
params.piv0._print_docs()
```

```{code-cell} ipython3
params.piv0.grid._print_docs()
```

Let's get an example of code to modify the parameters.

```{code-cell} ipython3
params.piv0._print_as_code()
```

Modifying a value is as simple as

```{code-cell} ipython3
params.piv0.grid.overlap = 0.2
```

```{code-cell} ipython3
params.piv0.grid
```

A spelling mistake is clearly annonced by a AttributeError:

```{code-cell} ipython3
try:
    params.piv0.grid.overlqp = 0.2
except AttributeError as e:
    print(e)
```
