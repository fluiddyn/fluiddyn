% FluidDyn documentation master file, created by
% sphinx-quickstart on Sun Mar  2 12:15:31 2014.

# FluidDyn documentation

```{raw} html
<h1 align="center">
  <img width="400" alt="FluidDyn logo"
  src="https://foss.heptapod.net/fluiddyn/fluiddyn/raw/branch/default/doc/logo.png">
</h1>
```

The FluidDyn project aims at promoting the use of open-source Python software in research
in fluid dynamics. The project provides some Python packages specialized for different
tasks, in particular

- [Transonic](http://transonic.readthedocs.org), to make your Python code fly at
  transonic speeds!
- [Fluidfft](http://fluidfft.readthedocs.org) for 2D and 3D Fast Fourier Transforms,
- [Fluidsim](http://fluidsim.readthedocs.org) for numerical simulations,
- [Fluidlab](http://fluidlab.readthedocs.org) for laboratory experiments,
- [Fluidimage](http://fluidimage.readthedocs.io) for processing of images of fluid,
- [Fluidsht](http://fluidsht.readthedocs.org) for Spherical Harmonic Transforms.
- [Formattex](https://foss.heptapod.net/fluiddyn/formattex) and
  [Formatbibtex](https://foss.heptapod.net/fluiddyn/formatbibtex) for Latex

This documentation presents the FluidDyn project and the package of the same name, which
is the base package on which the other packages depend on. For the specific
documentations of these specialized packages, follow the links above.

```{toctree}
---
caption: The FluidDyn project
maxdepth: 1
---
intro-motivations
advice_on_Python
```

## Metapaper and citation

If you use any of the FluidDyn packages to produce scientific articles, please cite
[our metapaper presenting the FluidDyn project and the fluiddyn package](https://openresearchsoftware.metajnl.com/articles/10.5334/jors.237/):

```
@article{fluiddyn,
doi = {10.5334/jors.237},
year = {2019},
publisher = {Ubiquity Press,  Ltd.},
volume = {7},
author = {Pierre Augier and Ashwin Vishnu Mohanan and Cyrille Bonamy},
title = {{FluidDyn}: A Python Open-Source Framework for Research and Teaching in Fluid Dynamics
    by Simulations,  Experiments and Data Processing},
journal = {Journal of Open Research Software}
}
```

```{toctree}
---
caption: User Guide of the fluiddyn package
maxdepth: 2
---
install
tutorials/overview
tutorials
```

### API Reference

Here is a presentation of the API of the fluiddyn package. If you are looking for a particular feature, you can also use
the "Quick search" tool in this page.

```{eval-rst}
.. autosummary::
   :toctree: generated/

   fluiddyn.io
   fluiddyn.util
   fluiddyn.clusters
   fluiddyn.output
   fluiddyn.calcul
```

Fluiddyn also provides a small package for documentation:

```{eval-rst}
.. autosummary::
   :toctree: generated/

   fluiddoc
```

```{toctree}
---
caption: More
maxdepth: 1
---
changes
advice_developers
code-of-conduct
to_do
authors
miscellaneous
```

### Links

- [Forge of the FluidDyn project on Heptapod](https://foss.heptapod.net/fluiddyn)
- [Forge of the fluiddyn package on Heptapod](https://foss.heptapod.net/fluiddyn/fluiddyn)
- [FluidDyn in PyPI](https://pypi.org/project/fluiddyn/)
- [FluidDyn project blog](https://fluiddyn.bitbucket.io/)
- FluidDyn user chat room in
  [riot](https://riot.im/app/#/room/#fluiddyn-users:matrix.org) or
  [slack](https://fluiddyn.slack.com)
- [FluidDyn mailing list](https://www.freelists.org/list/fluiddyn)
- [FluidDyn on Twitter](https://twitter.com/pyfluiddyn)
- [FluidDyn on Youtube](https://www.youtube.com/channel/UCPhRtVq1v4HtcecEdEOcXBw)

# Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
