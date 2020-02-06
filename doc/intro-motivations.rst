Introduction and motivations
============================

The FluidDyn project first emerges from the work of Pierre Augier, a researcher
in fluid dynamics strongly interesting by programming and open-source. Then,
:doc:`other people <authors>` worked on this collaborative project. However,
for this introduction, it is simpler for me (Pierre) to use I instead of we.
These are my ideas and it is clearer that people can use and develop FluidDyn
packages without sharing them.

For a better and less personal presentation, one can read `our metapaper
presenting the FluidDyn project and the fluiddyn package
<http://www.legi.grenoble-inp.fr/people/Pierre.Augier/docs/fluiddyn_metapaper.pdf>`_
(accepted by the `Journal of Open Research Software (JORS)
<https://openresearchsoftware.metajnl.com/>`_).

If you have any questions, comments or suggestions, please do not hesitate to
`fill an issue in the main repository
<https://foss.heptapod.net/fluiddyn/fluiddyn/issues>`_ or simply discuss with us on
our `chat rooms <https://fluiddyn.slack.com>`_.

How FluidDyn started
^^^^^^^^^^^^^^^^^^^^

Now, I am a CNRS researcher at LEGI (UGA, CNRS, in Grenoble) but I started to
work on FluidDyn when I was at KTH (Stockholm) and DAMTP (Cambridge).

I did my PhD on stratified turbulence and instabilities at LadHyx (Paris).
During my PhD years, I worked mainly with Bash, Fortran and Matlab. Some days
after my PhD defense in 2011, I was introduced by a couple of geek friends to a
funny programming language |:snake:| which could replace Matlab for what we did
with it.

I started to work with Python and to like it a lot. Python for sciences wasn't
what it is today but it was in many aspects much nicer than the infernal trio
Bash / Fortran / Matlab |:slight_smile:| (let's stress that Bash and
Fortran are great tools!).

By using Python (and reading/watching stuffs), I started to learn a lot about
programming, computers, software engineering and open-source. I also saw how
other scientific communities were using Python and scientific open-source
projects much more than in fluid dynamics, for example astrophysics (with in
particular `Astropy <http://www.astropy.org/>`_).

So I started to work on packages specialized for different aspects of my
research (fluidlab, fluidimage, fluidfft, fluidsim, ...). We also needed one
base package (called fluiddyn) to gather code useful for the specialized
packages.

Design Goals
^^^^^^^^^^^^

I work on the project FluidDyn first to have good tools for my research, where
I mainly do laboratory experiments, image analysis and numerical simulations.
My point of view is that to get good tools, they must really be "collaborative"
and built with the tools and methods of open-source dynamics.

So FluidDyn is also for me a way to contribute to launch a collaborative
dynamics in coding in the field of (geophysical) fluid dynamics. I see the
opportunities for my community of using open-source tools and methods. It seems
to me that we could greatly improve our global productivity since the way it
works now is really not optimal.

Numerics is everywhere in research: for numerical simulations but also for
analytic and experimental studies. Unfortunately, many researchers have
contempt for coding and software. Many very bad practices are so common that
there is a huge waste of time, energy, ideas and money! So many lines of code
are badly coded so they are surely full of bugs and of course not reusable. So
many pieces of code are lost when the PhD student who has written them goes
away.

A big change seems to be necessary but it is a real challenge.  First, the
organization of research does not help...  The competition between researchers,
groups and universities is strong, which discourage collaborations and
planning in the community.

Then, bad habits are difficult to give up, especially when they are efficient
on the short range and when the bosses in research feel uncomfortable with new
tools and methods.

The example of the dominant languages/tools is interesting. Bash (or even csh,
with awk and sed) should be used only for very specific and simple tasks.
Compiled languages (Fortran, C and C++) should not be used for everything. Even
though the commercial programs like Matlab or Labview can be useful and
efficient for individuals and groups, they have huge limitations (in particular
for collaborations) and are for the community a problem.

Finally, education is also an issue. It is interesting to see universities,
institutes and laboratories paying big amounts of money to be able to use
Matlab and Labview for research and at the same time learning these tools to
their students instead of open-source alternatives.

I think open-source, Python and its scientific environment are a great
opportunity for science and fluid dynamics. FluidDyn is a tool to test this
hypothesis and to increase equality, freedom and efficiency in fluid dynamics
with open-source methods.

Open-source
^^^^^^^^^^^

FluidDyn is an open-source project. The package fluidyn is distributed under
the CeCILL-B_ License, a BSD compatible french license done in particular by
the `CNRS <http://www.cnrs.fr/>`_.

.. _CeCILL-B: http://www.cecill.info/index.en.html


Python programming language
^^^^^^^^^^^^^^^^^^^^^^^^^^^

FluidDyn is mostly a set of Python packages. They are written mostly in Python
with also small bits of Cython, C and C++. Since it is still necessary to
convince some people in the field that it is efficient to use Python, here is a
list of some reasons for using this language in research.

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

Documented and tested
^^^^^^^^^^^^^^^^^^^^^

The FluidDyn project is a framework for developing research codes. It should
show good practices and clean examples. It has also to be quite stable and
sure. Therefore, a lot of effort is put in having unit tests and a quite good
documentation with examples and tutorials.

Why specialized in fluids?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Many tasks that can be done using FluidDyn are not specific to fluid dynamics
research. But it is simpler to write a more specific software so FluidDyn is
first thought to be used specifically for fluid dynamics.

There are other specific Python packages for other subjects, like astronomy
(`Astropy <http://www.astropy.org/>`_) and biology (`Biopython
<http://biopython.org>`_).
