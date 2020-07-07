:orphan:

Creating news fragments
=======================

This directory contains "news fragments" which are short files that contain a
small **ReST**-formatted text that will be added to the next what's new page.

Make sure to use full sentences with correct case and punctuation, and please
try to use Sphinx intersphinx using backticks. The fragment contains a few
bullet points of the change.

Each file should be named like ``<MERGE REQUEST>.<TYPE>``, where
``<MERGE REQUEST>`` is a merge request number, and ``<TYPE>`` is one of:

==============  ==============================================
Type            Purpose
==============  ==============================================
``added``       Added for new features
``changed``     Changed for changes in existing functionality
``deprecated``  Deprecated for soon-to-be removed features.
``removed``     Removed for now removed features.
``fixed``       Fixed for any bug fixes.
``security``    Security in case of vulnerabilities.
==============  ==============================================

Create it as follows::

    towncrier create 123.changed

Most categories should be formatted as paragraphs with a heading.
So for example: ``123.changed`` would have the content::

    ``my_new`` option for `my_favorite_function`

    - The ``my_new`` option is now available for `my_favorite_function`.
    - To use it, write ``my_module.my_favorite_function(..., my_new=True)``.

The first line should be short and the longer details should be added as bullet
points. The formatting is taken care of by the template.

Note the use of single-backticks to get an internal link (assuming
``my_favorite_function`` is exported from the package namespace),
and double-backticks for code.

If you are unsure what merge request type to use, don't hesitate to ask in your
MR.

You can install ``towncrier`` and run ``towncrier build --draft --version 0.3.4``
if you want to get a preview of how your change will look in the final release
notes.

.. note::

    This README was adapted from the pytest changelog readme under the terms of
    the MIT licence.

