General advice on how to work with Python
=========================================

Read!
-----

- If you have only weak knowledge on Python, start with the `the
  official Python tutorial
  <https://docs.python.org/2/tutorial/index.html>`_.

- It is always useful to have a look at `the official Python
  documentation <https://www.python.org/doc/>`_.

- If you already know Python, it could be useful to check out some
  `best practices <http://docs.python-guide.org/en/latest/>`_ and to
  have a look at the famous book `Dive in Python
  <http://www.diveintopython.net/>`_ (and now `Dive in Python 3
  <http://www.diveintopython3.net/>`_.

- If you begin with Python and even if you have some experience with
  this language, `understanding Python variables
  <http://foobarnbaz.com/2012/07/08/understanding-python-variables/>`_
  is important and can avoid some bugs.


Use fly checks and a good editor!
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

If you like integrated development environment, you can for example
use `Spyder <https://github.com/spyder-ide/spyder>`_ (Scientific
PYthon Development EnviRonment). Note that Spyder has to be setup
correctly to use fly checks.

Another good solution is `Emacs
<https://www.gnu.org/software/emacs/>`_, but it should be setup
correctly (for example with `Flycheck
<http://flycheck.readthedocs.org>`_, see `my Emacs
configuration <https://bitbucket.org/fluiddyn/fluid_emacs.d>`_).


Note that code checkers can also be used outside of the editor, for
example with pylint. we can use the commands (from the FluidDyn root
directory)::

  pylint fluiddyn
  pylint -E fluiddyn.lab.probes
  pylint --help-msg=no-member


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


Use virtualenv
--------------

It is a good idea to use a virtual environment. With `virtualenv
<https://virtualenv.pypa.io>`_ it is very easy. I do something like
this::

  MYPY=$HOME/path/mypy
  mkdir -p $MYPY
  virtualenv --system-site-packages $MYPY

Then I have a non-executable script ``load_mypy.sh`` in the directory
~/bin with something like this::

  export VIRTUAL_ENV_DISABLE_PROMPT=0
  MYPY=$HOME/path/mypy
  source $MYPY/bin/activate

This script should be use by `source ~/bin/load_mypy.sh` so you can
have a line with `alias load_mypython='source ~/bin/load_mypy.sh'` in the
file ~/.bash_aliases.

Remark: it could also be convenient to use the ``module load ...``
procedure...


For Matlab users
----------------

If you begin with Python and you really like Matlab, I would advice to
add in your ``.bashrc`` the line::

  alias ipython='ipython --pylab'

With the option ``--pylab``, Ipython imports the module
``matplolib.pylab`` with the command ``from matplotlib.pylab import
*`` and runs ``matplotlib.pylab.ion()`` [1]_ (this can take a few
seconds), so the iterative Python console will behave much more like
in Matlab than the standard ipython console without ``pylab``
imported.


Python 2.7 and Python 3
^^^^^^^^^^^^^^^^^^^^^^^

Python 3 is cleaner and better but still significantly slower... In
2014, I think we have to try to write Python 2-3 compatible code (with
some ``try`` and ``from __future__`` statements and using for example
the package `future <http://python-future.org/>`_)... but then that we
can continue to run the program with Python 2.7.


---------------------------------------------

.. [1] In your scripts, it is better to use ``import matplotlib.pyplot as plt``.
