General overview
================

This document is a work in progress. If you have any questions, comments or
suggestions, please send them to me (pierre.augier (AT) legi.cnrs.fr).

The project FluidDyn
--------------------

Design Goals
^^^^^^^^^^^^

I work on the project FluidDyn first to have good tools for my research. But it
is also for me a way to contribute to launch a collaborative dynamics in coding
in the field of (geophysical) fluid dynamics. I see the opportunities for my
community of using tools and methods of the open-source world. It seems to me
that we could greatly improve our global productivity since the way it works
now is so bad.

Numerics is everywhere in research: for numerical simulations but also for
analytic and experimental studies.  Unfortunately, many researchers have
contempt for coding and software.  Many very bad practices are so common that
there is a huge waste of time, energy, ideas and money!  So many lines of code
are badly coded so they are surely full of bugs and of course not reusable.  So
many pieces of code are lost when the PhD student who has written them goes
away.

A big change seems to be necessary but it is a real challenge.  First, the
organization of research does not help...  The competition between researchers,
groups and universities is strong, which can discourage collaborations and
planning in the community.

Then, bad habits are difficult to give up, especially when they are efficient
on the short range and when the bosses in research feel uncomfortable with new
tools and methods.

The example of the dominant languages/tools is interesting.  Bash (or even csh,
with awk and sed)  should be used only for very specific and simple tasks.
Compiled languages (Fortran, C and C++) should not be used for everything.
Even though the commercial programs like Matlab or Labview can be useful and
efficient for individuals and groups, they have huge limitations and are for
the community a problem.

Finally, education is also a big issue.  It is incredible to see universities,
institutes and laboratories paying big amounts of money to be able to use
Matlab for research and at the same time spending a lot of effort to learn
Matlab to their students.

We need a dynamics in open-source coding in science and in particular in fluid
dynamics. I think Python and its scientific environment is a great opportunity
for us. FluidDyn is a tool to test this hypothesis and to increase equality,
freedom and efficiency in fluid dynamics with open-source methods.

Open-source
^^^^^^^^^^^

FluidDyn is an open-source project. The package fluidyn is distributed under
the CeCILL-B_ License, a BSD compatible french license done in particular by
the `CNRS <http://www.cnrs.fr/>`_.

.. _CeCILL-B: http://www.cecill.info/index.en.html


Python programming language
^^^^^^^^^^^^^^^^^^^^^^^^^^^

FluidDyn is mostly a set of Python packages. They are written mostly in Python
with also small bits of Cython, C and C++.  Since it is still necessary to
convince some people in the field that it is a good idea to use Python, here is
a list of some reasons for using this language in research.

- **Free and open-source**: the main implementations of the language
  (Cpython, PyPy, etc.) and the libraries.

- **Clear and easily readable code by structure.**

- **Easy to learn**: good documentation, intuitive syntax and "There
  should be one-- and preferably only one --obvious way to do it"
  principle.

- **Multi-paradigm programming language**: sequential, object-oriented and
  functional.

- **Portability**: Linux-GNU, Unix in general so Mac OS and also
  Windows!

- **Simple install procedure for packages.**

- **General-purpose useful outside science**: from simple scripting
  to complex object-oriented software and web development (for example
  Youtube and Dropbox are written in Python). Thus it is very useful
  to learn Python.

- **Large and professional community.**

- **Easy to optimise**, in particular with profiling tools (cProfile,
  pstats) and Python "compilers" like `Cython <http://cython.org/>`_ and
  `Pythran <http://pythonhosted.org/pythran/>`_.

- **Easily extended with modules written in C, C++ or Fortran.**

- **Easy to implement tests** (`unittest
  <https://docs.python.org/3.4/library/unittest.html#module-unittest>`_).

- **Many scientific libraries and software**:

  * `SciPy <http://www.scipy.org/>`_: fundamental library for scientific
    computing,
    
  * NumPy: base N-dimensional array package,

  * Matplotlib: comprehensive 2D Plotting,

  * IPython: enhanced Interactive Console,

  * Sympy: symbolic mathematics,

  * Pandas: data structures & analysis,

  * h5py: pythonic interface to the HDF5 binary data format.

  * mpi4py: MPI for Python.


If you use Matlab, these comparisons can be interesting:

- http://www.pyzo.org/python_vs_matlab.html.

- http://phillipmfeldman.org/Python/Advantages_of_Python_Over_Matlab.html

Simplicity
^^^^^^^^^^

The FluidDyn packages are written to be easy-to-use and nice to develop.  The
object-oriented development is very interesting in this respect.  In particular
experiments and simulations are represented by objects, which are easy to
create, load, filter, select and loop over.

Example: the data files contains information to be loaded. Thus, it should be
possible to create an object associated with the data in a file by running::

    import fluiddyn as fld
    torque = fld.create_object_from_file(str_file='torque_*_2014-26')

Documented and tested
^^^^^^^^^^^^^^^^^^^^^

The FluidDyn project is a framework for developing research codes. It should
show good practices and clean examples. It has also to be quite stable and
sure. Therefore, a lot of effort is put in having unit tests and a quite good
documentation with examples and tutorials.

Why fluids?
^^^^^^^^^^^

Many tasks that can be done using FluidDyn are not specific to fluid dynamics
research. But it is simpler to write a more specific software so FluidDyn is
first thought to be used specifically for fluid dynamics.

There are other specific Python packages for astronomy (`Astropy
<http://www.astropy.org/>`_) and biology (`Biopython
<http://biopython.org>`_).


Why experiments and numerics?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Experiments and numerics share common tools and common methods. It is very
fruitful to connect these two approaches and therefore, they have to work
together.


Main features of the base package fluiddyn
------------------------------------------

The base package fluiddyn provides utilities for

- :ref:`input-output in different file formats <io>`

- making :ref:`figures <output>`

- launching jobs on :ref:`clusters <clusters>`

- storing parameters.

- handling series of files.
