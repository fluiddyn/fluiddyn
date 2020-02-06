Advice on how to work with Python
=================================

FluidDyn should be used also by scientists that are not experienced in Python.
We provide some advice on how to work with Python and how to get a good Python
environment.

Use an up-to-date Python environment!
-------------------------------------

Python is an old language but the strong dynamics in scientific Python is quite
young. The base packages have greatly improved these last years so it is really
better to use recent versions. Therefore, it is not a good idea to use
scientific python libraries packaged in not very recent Linux versions.

.. toctree::
   :maxdepth: 1

   get_good_Python_env

Read and watch!
---------------

- If you have only basic knowledge on Python, start with the `the official
  Python tutorial <https://docs.python.org/3/tutorial/index.html>`_.

- It is always useful to have a look at `the official Python documentation
  <https://www.python.org/doc/>`_.

- If you already know Python, it could be useful to check out some `best
  practices <http://docs.python-guide.org/en/latest/>`_ and to have a look at
  the famous book `Dive in Python 3 <http://www.diveintopython3.net/>`_.

- If you begin with Python and even if you have some experience with
  this language, `understanding Python variables
  <http://foobarnbaz.com/2012/07/08/understanding-python-variables/>`_
  is important and can avoid some bugs.

- http://www.scipy-lectures.org/

There are also plenty interesting Python videos on the web...


Don't use Python 2.7 and try to use Python >= 3.6
-------------------------------------------------

If you still use Python 2.7 in 2019, it is time to stop! In few months, Python
2.7 won't be supported anymore by the CPython developers
(https://pythonclock.org/) and a number of critical Python projects have
`pledged to stop supporting Python 2 soon <https://python3statement.org/>`_.

We even strongly advice to stop using Python < 3.6. Conda and pyenv are very
convenient to use recent versions of Python in most systems (see :doc:`Get a
good scientific Python environment <get_good_Python_env>`).

With Python 3.6, one can use `f-strings
<https://www.python.org/dev/peps/pep-0498/>`_ and the support for `pathlib
<https://docs.python.org/3/library/pathlib.html>`_ is much better. These are
the reasons why we decided to support only Python >= 3.6 for the FluidDyn
packages.


Use a good editor with fly checks
---------------------------------

Python is a very dynamics language. It is very nice but it is also
very dangerous. A silly error (a misspell for example) is very easy
and there is no compiler to tell you that something is
wrong. Automatic checking of the code is enough to avoid most of these
silly errors so anyone has to use it.

The style in Python is also really important (see below) so any Python
developer has to get used to code properly. The best way is to code
with a fly checker that tells you as soon as you do something wrong.

Most experienced Python programmers use an good Python editor with fly
checking and it is really very useful. So of course beginners have to
use a good Python editor running fly checks!

For scientists and for simpler programming (only scripts), you can for example
use `Spyder <https://github.com/spyder-ide/spyder>`_ (Scientific PYthon
Development EnviRonment). Note that Spyder has to be setup correctly to use fly
checks.

`Visual studio code <https://code.visualstudio.com/>`_ is great for more
advanced programming (with at least the `Python
<https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_ and
`Settings Sync
<https://marketplace.visualstudio.com/items?itemName=Shan.code-settings-sync>`_
extensions). For developping a Python package, it is indeed very good and it
really improves productivity and even the quality of the code, see for example
this `blog post by Kenneth Reitz
<https://www.kennethreitz.org/essays/why-you-should-use-vs-code-if-youre-a-python-developer>`_.
On Unix, one may want to avoid using a binary built by Microsoft so we can use
`vscodium <https://github.com/VSCodium/vscodium>`_.

Another GNUer solution is `Emacs <https://www.gnu.org/software/emacs/>`_, but
it should be setup correctly (for example with `Flycheck
<http://flycheck.readthedocs.org>`_, see `my Emacs configuration
<https://foss.heptapod.net/fluiddyn/fluid_emacs.d>`_).


The style is important
----------------------

Most of the time, we have to follow the Style Guide for Python Code,
the so-called `"pep 8" <https://www.python.org/dev/peps/pep-0008/>`_).
It is not just for fun. On the long term, it really helps.

In particular,

- limit all lines to a maximum of 79 characters.
- most of the time, comments before the code. At least not in very
  long lines of more than 79 characters.
- names of the modules in lower case.
- names of the classes in CamelCase, i.e. LikeThis.
- no space before a comma and a space after.
- no tabulation! four spaces.
- no trailing white space.
- documentation of the functions in a docstring.
- Python is in English. It is a good idea to write Python modules all
  in English.

For FluidDyn packages, we use `black <https://github.com/ambv/black>`_ with the
command ``black -l 82``.


For Matlab users
----------------

If you begin with Python and you really like Matlab, I would advice to
add in your ``.bashrc`` the line::

  alias ipython='ipython --pylab'

With the option ``--pylab``, Ipython imports the module ``matplolib.pylab``
with the command ``from matplotlib.pylab import *`` and runs
``matplotlib.pylab.ion()`` (this can take a few seconds), so the iterative
Python console will behave much more like in Matlab than the standard ipython
console without ``pylab`` imported.

In contrast, in you script, do not use the devil line ``from matplotlib.pylab
import *``. It is much better to learn how to use matplotlib with the import
``import matplotlib.pyplot as plt``.
