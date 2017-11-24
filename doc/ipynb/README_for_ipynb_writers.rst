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


It is therefor important not to commit the executed versions of the notebooks.

The command ``fluidnbstripout ipynb`` (or Make nbstripout) has to be used before
any commit when notebooks have been executed manually.

Some notebooks can not be executed during the build process, for example
because it won't work in the readthedocs server or because they necessitate
human interaction (as for the notebook ``executed/query.ipynb``). These notebooks
has to be put in the directory ``executed``.
