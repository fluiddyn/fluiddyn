README for notebook writers
===========================

Dear fluiddyn notebook writers,

Notebooks in this directory are processed with the function
:func:`fluiddoc.ipynb_maker.ipynb_to_rst` called in the file ``doc/conf.py``
(which is executed during the doc building).

Unless explicitly mentioned in the call of ipynb_to_rst, the notebooks are
executed.

.. code-block:: python

  ipynb_to_rst()
  ipynb_to_rst('ipynb/executed', executed=True)


It is therefore important not to commit the executed versions of the notebooks.

The command ``fluidnbstripout ipynb`` (or Make nbstripout) has to be used before
any commit when notebooks have been executed manually.

Some notebooks can not be executed during the build process, for example
because it won't work in the readthedocs server or because they necessitate
human interaction (as for the notebook ``executed/query.ipynb``). These notebooks
has to be put in the directory ``executed``.

Alternative setup
-----------------
The `Executable Books`_ project and the MyST toolchain is another convenient
way to produce documentation from Jupyter notebooks. To do so install::

    myst-nb
    sphinx-copybutton  # optional

.. _Executable Books: https://executablebooks.org/

And then in sphinx ``conf.py`` file, add the following:

.. code-block:: ipython3

   import os


   extensions = [
       "myst_nb",
       "sphinx_copybutton"
   ]

   # Execute ipynb files into with a cache ...
   jupyter_execute_notebooks = "cache"
   jupyter_cache = "./_build/jupyter_cache"
   os.makedirs(jupyter_cache, exist_ok=True)
   # ... except these ipynb files
   execution_excludepatterns = ['ipynb/executed/*']

   # CSS selector which modifies the sphinx-copybutton feature
   copybutton_selector = ",".join(
       [
           f"div.highlight-{css_class} div.highlight pre"
           for css_class in ("python", "ipython3", "default")
       ]
   )

   # The suffix of source filenames.
   source_suffix = {
       '.rst': 'restructuredtext',
       '.ipynb': 'myst-nb',
       '.myst': 'myst-nb',
   }
