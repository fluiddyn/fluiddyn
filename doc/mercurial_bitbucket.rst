Mercurial and Bitbucket short tutorial for FluidDyn
===================================================

`Mercurial <http://mercurial.selenic.com/>`_ is a free, distributed
source control management tool. It's is a great tool and if you are
doing research (coding and/or writing papers), you should use a
version control software! It seems to me that Mercurial is a good
solution for researchers (in particular it is simpler to learn than
Git).

Mercurial couples very well with the programs TortoiseHG and Meld (if
you can, just install them) and with the site `Bitbucket
<https://bitbucket.org>`_.

There are a lot of tutorials and documentations about Mercurial and
Bitbucket (for example `the official Mercurial tutorial
<http://mercurial.selenic.com/wiki/Tutorial>`_ or `here
<http://www.math.wisc.edu/~jeanluc/bitbucket_instructions.php>`_). In
this page, I focus on what is needed to use and develop FluidDyn.


Set-up Mercurial
----------------

Install Mercurial and create a file ``~/.hgrc`` with something like::

  [ui]
  username=myusername  <email@adress.org>
  editor=emacs -nw

  [web]
  cacerts = /etc/ssl/certs/ca-certificates.crt

  [extensions]
  color =
  hgext.extdiff =

  [extdiff]
  cmd.meld =

Get help
--------

Get help::

  hg help

or for a specific command (here ``clone``)::

  hg help clone

Get the FluidDyn repository
---------------------------

There are at least two methods...

1. Create your own FluidDyn repository on Bitbucket. 

   Go to the page of the main repository. Create your own FluidDyn
   repository on Bitbucket by clicking on Fork. Then from the page of
   your repository, click on Clone, copy the given command line and
   run it from the directory where you want to have the root directory
   of FluidDyn.

2. Go where you want to have the root directory of FluidDyn and run::

     hg clone https://bitbucket.org/fluiddyn/fluiddyn

   Then modify the file .hg/hgrc in the created directory.

Workflow
--------

We have already seen the command ``hg clone``.

To get a summary of the working directory state::

  hg summary

To show changed files in the working directory::

  hg status

or just ``hg st``.

If you add new files or if you deleted files::

  hg add name_of_the_file

  hg remove name_of_the_file

This command is also very usefull::

  hg addre


Each time you did some consistent changes::

  hg commit

I would advice to follow this command with a ``hg st`` to verify that
you did what you wanted to do. If you are unhappy with this commit,
you can cancel it with (be careful)::

  hg rollback

To push the state of your working repository to your Bitbucket repository::

  hg push

The inverse command is::

  hg pull


Create a repository from nothing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new repository in the given directory by doing::

  hg init
