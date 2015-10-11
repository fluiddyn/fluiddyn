General overview
================

This document is very much a work in progress. If you have any
questions, comments, complaints, or suggestions, please send them to
me (pierre.augier (AT) legi.cnrs.fr).

Design Goals
------------

FluidDyn is for me a first step to try to start a collaborative
dynamics for coding in the field of (geophysical) fluid dynamics.

..
   Apart from using a nice tool, I started the FluidDyn project in order
   to increase the global productivity of researchers in the field of
   fluid dynamics and finally to help to do together better research.

   Numerics is everywhere in research. Of course numerical simulations
   but also for analytical work and experiment studies. However, to do
   good research, it is better not to lose time on the numerics and to
   think to the problem you study rather than to the numerics.

   If we consider the way the scientific community works on developing
   tools for research, there is a huge waste of time, energy, ideas and
   money! So many lines of code are badly coded, for example in a way
   they can not be reused.. So many ideas are rewritten so many times. So
   many pieces of code are lost when the PhD that have written them go
   away.

   There are many reasons for that. The organisation of research does not
   help... The competition between researchers, groups and universities
   is strong, which can discourage collaborations and planning in the
   community. But there is also and maybe mainly technical reasons.  The
   languages: Bash (with awk, sed and co...), compiled languages (mostly
   fortran, C and C++) and company software like Matlab.


Open-source
^^^^^^^^^^^

FluidDyn is an open-source software distributed under the CeCILL-B_
License, a BSD compatible french license.

.. _CeCILL-B: http://www.cecill.info/index.en.html


Python programming language
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since it is still necessary to convince some people in the field that
it is a good idea to use Python, here is a list of some reasons for
using this language in research.

- **Free and open-source**: the main implementations of the language
  (Cpython, PyPy, etc.) and the libraries.

- **Clear and easily readable code by structure.**

- **Easy to learn**: good documentation, intuitive syntax and "There
  should be one-- and preferably only one --obvious way to do it"
  principle.

- **Multi-paradigm programming language**: in particular object-oriented,
  functional and sequential.

- **Portability**: Linux-GNU, Unix in general so Mac OS and also
  Windows!

- **Normalised and very simple install procedure.**

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

  * ...


If you use Matlab, these comparisons can be interesting:

- http://www.pyzo.org/python_vs_matlab.html.

- http://phillipmfeldman.org/Python/Advantages_of_Python_Over_Matlab.html


Presentation
------------

The FluidDyn project is a framework for developing research codes. It
should show good practices and clean examples.


Main features
^^^^^^^^^^^^^

The package fluiddyn provides utilities for

- :ref:`input-output in different file formats <io>`

- making :ref:`figures, movies, ... <output>`

Other specialized packages are part of the FluidDyn project:

- `fluidsim <https://pypi.python.org/pypi/fluidsim>`_ (see the
  `documentation <http://fluidsim.readthedocs.org>`__)

- `fluidlab <https://pypi.python.org/pypi/fluidlab>`_ (see the
  `documentation <http://fluidlab.readthedocs.org>`_)

  

..
   - :ref:`working in the laboratory <lab>`

     * using :ref:`acquisition boards <lab.boards>`

     * controlling devices as :ref:`tanks <tanks>`, :ref:`pumps <pumps>`, ...

     * working with a Raspberry Pi,

     * doing relatively complex :ref:`experiments <exp>`,

     * ...

   - :ref:`numerical simulations <simul>`

     * ...

     * ...





Simplicity
^^^^^^^^^^

Object-oriented... In particular experiments and simulations are
represented by objects. Easy to create, load, filter, select, loop
over, ...


Example: the files contains information to be loaded. Thus, it should
be possible to create an object associated with the data in a file
by running::

    torque = fld.create_object_from_file(str_file='torque_*_2014-26')



Documented and tested
^^^^^^^^^^^^^^^^^^^^^

Importance of documentation and testing functions.


Why fluids?
^^^^^^^^^^^

Many tasks that can be done using FluidDyn are not specific to fluid
dynamics research. But it is simpler to write a more specific software
so FluidDyn is first thought to be used specifically for the study of
fluid dynamics.

There are other specific Python packages for astronomy (`Astropy
<http://www.astropy.org/>`_) and biology (`Biopython
<http://biopython.org>`_).


Why experiments and numerics?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Common tools, common methods. Has to work together. Fruitful to
connect.

