Mercurial and Bitbucket short tutorial for FluidDyn
===================================================

`Mercurial <http://mercurial.selenic.com/>`_ is a free, distributed source
control management tool. It's is a great tool and if you are doing research
(coding and/or writing papers), you should use a version control software! It
seems to me that Mercurial is a good solution for researchers (in particular it
is in my opinion simpler and nicer to learn and use than Git).

Mercurial couples very well with the programs TortoiseHG and Meld (if you can,
just install them, especially Meld) and with the site `Bitbucket
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
  hggit =

  [extdiff]
  cmd.meld =

The line starting with hggit is optional and enables the extension `hg-git
<http://hg-git.github.io/>`_. This extension is useful in particular to work
with Github and Gitlab.

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

or just ``hg sum``.

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

or::

  hg commit -m "A message explaining the commit"

I would advice to run after a commit command ``hg st`` to check that you did
what you wanted to do. If you are unhappy with the commit, you can amend it
with another commit with::

  hg commit --amend

To push the state of your working repository to your Bitbucket repository::

  hg push

The inverse command (pull all commits from the remote repository) is::

  hg pull


Create a repository from nothing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new repository in the given directory by doing::

  hg init


Working with hggit and github
-----------------------------

To clone a git repository::

  hg clone git+ssh://git@github.com/serge-sans-paille/pythran.git

Git branches are represented as Mercurial bookmarks so such commands can be
usefull::

  hg log --graph

  hg up master

  hg help bookmarks
  hg bookmarks
  hg bookmark master

Remark: ``bookmarks`` and ``bookmark`` correspond to the same mercurial
command.

For fluiddyn developers, we can add in the file ``.hg/hgrc`` something like::

  [paths]
  default = https://paugier@bitbucket.org/fluiddyn/fluidimage
  github = git+ssh://git@github.com/fluiddyn/fluidimage

Do not forget to place the bookmark ``master`` as wanted.

Forget a bad commit
-------------------

A bad commit that you want to forget... First find the revision number of
the last good commit::

  hg log --graph

Let's say that it is 180 and that there are actually two bad commits (181 and
182). Update to the last good revision::

  hg up 180

You may have to add the ``--clean`` (``-C``) option. Commit something from here
(you need to modify something)::

  hg commit -m "New commit from the last good commit"

You have just created another head (unnamed branch). You can see this with::

  hg heads

Then back to the last bad commit (let's say it's 182)::

  hg up 182

To close this bad branch::

  hg commit --close-branch -m "Commit to close the bad branch"

And finally we come back to the last commit::

  hg up default

(in Mercurial ``default`` is the name of the default branch, as ``master`` for
Git) and we check that everything is ok::

  hg sum
  hg log --graph
