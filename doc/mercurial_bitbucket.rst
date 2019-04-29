Mercurial and Bitbucket short tutorial for FluidDyn
===================================================

`Mercurial <http://mercurial.selenic.com/>`_ is a free, distributed source
control management tool. It's is a great tool and if you are doing research
(coding and/or writing papers), you should use a version control software! It
seems to me that Mercurial is a good solution for researchers (in particular it
is in my opinion simpler and nicer to learn and use than `Git
<https://www.mercurial-scm.org/wiki/GitConcepts>`_).

Mercurial couples very well with the programs TortoiseHG and Meld (if you can,
just install them, especially Meld) and with the site `Bitbucket
<https://bitbucket.org>`_.

There are a lot of tutorials and documentations about Mercurial and
Bitbucket (for example `the official Mercurial tutorial
<http://mercurial.selenic.com/wiki/Tutorial>`_ or `here
<http://www.math.wisc.edu/~jeanluc/bitbucket_instructions.php>`_). In
this page, I focus on what is needed to use and develop FluidDyn.

Installation
------------

To install Mercurial with few important extensions, I usually do on Linux::

  pip2 install mercurial hg-git hg-evolve -U --user

On Windows, macOS and Linux, one can use conda to install Mercurial with few
extensions::

  conda config --add channels conda-forge
  conda create -n env_hg mercurial-app
  conda activate env_hg
  pip install hg+https://bitbucket.org/durin42/hg-git

To get the command ``hg`` available in other terminals, we need to run:

- On Unix and with Bash::

    APP_DIR=$HOME/.local/bin/bin-conda-app/
    mkdir -p $APP_DIR
    echo -e "\nexport PATH=\$PATH:$APP_DIR\n" >> ~/.bashrc
    ln -s $(which hg) $APP_DIR/hg

- On Unix and with Fish::

    set APP_DIR $HOME/.local/bin/bin-conda-app/
    mkdir -p $APP_DIR
    echo -e "\nset -gx PATH \$PATH $APP_DIR\n" >> ~/.config/fish/config.fish
    ln -s (which hg) $APP_DIR/hg

- On Windows in the conda prompt:

  ???

Set-up Mercurial
----------------

You need to create a file ``~/.hgrc``. For a good starting point, you can use
the command::

  hg config --edit

A example of configuration file::

  [ui]
  username=myusername <email@adress.org>
  editor=emacs -nw
  tweakdefaults = True

  [extensions]
  hgext.extdiff =
  # only to use Mercurial with GitHub and Gitlab
  hggit =
  # more advanced extensions
  churn =
  shelve =
  rebase =
  absorb =
  evolve =
  topic =

  [extdiff]
  cmd.meld =

The line starting with hggit is optional and enables the extension `hg-git
<http://hg-git.github.io/>`_. This extension is useful to work on projects
using Git, for example hosted on Github and Gitlab.

The extensions churn, shelve, rebase, absorb, evolve and topic are very useful
for more advanced users. Note that `evolve
<https://www.mercurial-scm.org/doc/evolution/>`_ and `topic
<https://www.mercurial-scm.org/doc/evolution/tutorials/topic-tutorial.html>`_
comes from the package `hg-evolve <https://pypi.org/project/hg-evolve>`_.

Get help
--------

Get help::

  hg help

or for a specific command (here ``clone``)::

  hg help clone

Simple workflow
---------------

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

Get the last version of a code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First pull all the changesets from the remote repository::

  hg pull

Then update the code to the tip::

  hg update

or just ``hg up``. You can also directly do::

  hg pull -u

Read the history
^^^^^^^^^^^^^^^^

You can get a list of the changesets with::

  hg log --graph

or just ``hg log -G``. With the ``--graph`` or ``-G`` option, the revisions are
shown as an ASCII art.

Update the code to an old revision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``hg up 220`` to update to the revision 220. We can use a tag, bookmark,
topic name or branch name instead of a number. To get a clean copy, add the
option ``-C`` (beware).


Create a repository from nothing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new repository in the given directory by doing::

  hg init


Pull-request based workflow with hg-evolve
------------------------------------------

We now use a PR based workflow for the development of FluidDyn packages with
main publishing repositories (for example
https://bitbucket.org/fluiddyn/fluidsim) and development non-publishing
repositories (for example https://bitbucket.org/paugier/fluidsim).

The new commits are pushed in the development repositories and developers have
to create Pull Requests (PR) to get things merged in the main repositories.

The first thing to do to start to develop something in one of the FluidDyn
repository is to create your own repository on Bitbucket. Go to the page of the
main repository of the package (for example for fluidsim,
https://bitbucket.org/fluiddyn/fluidsim). Create your own repository on
Bitbucket by clicking on Fork. Then from the page of your repository, click on
Clone, copy the given command line and run it from the directory where you want
to have the root directory of the repository.

.. tip ::

  FluidDyn developers can add in ``.hg/hgrc`` in their local repositories
  something like (replace ``paugier`` by your Bitbucket login)::

    [paths]
    default = ssh://hg@bitbucket.org/paugier/fluidsim
    fluiddyn = ssh://hg@bitbucket.org/fluiddyn/fluidsim

  and in ``~/.hgrc``::

    [alias]
    start_new_work = !hg pull fluiddyn && hg up -r $(hg identify --id fluiddyn)

  Then, one can run ``hg start_new_work`` to be sure to start a new development
  from the right commit.

Then, you can modify and add things. Create changesets using ``hg clone``, push
them in your repository in Bitbucket. Once you have something coherent, create
a PR on the Bitbucket website.

It's strongly adviced to enable the Bitbucket Pipelines for the development
repositories (for paugier/fluidsim, here
https://bitbucket.org/paugier/fluidsim/admin/addon/admin/pipelines/settings),
so that we know if the tests pass or fail.

We strongly advice to install and activate the `evolve
<https://www.mercurial-scm.org/doc/evolution/>`_ and `absorb
<https://gregoryszorc.com/blog/2018/11/05/absorbing-commit-changes-in-mercurial-4.8/>`_
extensions locally (see the example of ``.hgrc`` above) and to activate the
experimental support of evolve in Bitbucket (here
https://bitbucket.org/account/admin/features/). This gives a very nice user
experience for the PRs, with the ability to modify a PR with ``hg absorb`` and
safe history editing. NOTE that you have to use ssh pushes (because there is `a
bug for https pushes
<https://bitbucket.org/site/master/issues/17123/mercurial-obsolescence-markers-seem-to-be>`_)!

.. tip ::

  ``hg absorb`` is very useful during code review. Let say that a developer
  submitted a PR containing few commits. As explained in `this blog post
  <https://gregoryszorc.com/blog/2018/11/05/absorbing-commit-changes-in-mercurial-4.8/>`_,
  ``hg absorb`` is a mechanism to automatically and intelligently incorporate
  uncommitted changes into prior commits. Edit the files to take into account
  the remarks of the code review and just run::

    hg absorb
    hg push

  and the PR is updated!

.. note ::

  Advanced users can also take advantage of the `topic extension
  <https://www.mercurial-scm.org/doc/evolution/tutorials/topic-tutorial.html>`_,
  which is especially useful when one has to work on different PRs for the same
  repository "at the same time" (lightweight branching with multiple heads,
  better than bookmarks).


Working with hggit and Github
-----------------------------

To clone a git repository::

  hg clone git+ssh://git@github.com/serge-sans-paille/pythran.git

or just::

  hg clone https://github.com/serge-sans-paille/pythran.git

Git branches are represented as Mercurial bookmarks so such commands can be
usefull::

  hg log --graph

  hg up master

  hg help bookmarks

  # list the bookmarks
  hg bookmarks

  # put the bookmark master where you are
  hg book master

  # deactivate the active bookmark (-i like --inactive)
  hg book -i

.. note ::

  ``bookmarks``, ``bookmark`` and ``book`` correspond to the same
  mercurial command.

.. warning ::

  If a bookmark is active, ``hg pull -u`` or ``hg up`` will move the bookmark
  to the tip of the active branch. You may not want that so it is important to
  always deactivate an unused bookmark with ``hg book -i`` or with ``hg up
  master``.

Do not forget to place the bookmark ``master`` as wanted.

.. warning ::

  For fluiddyn core developers, we can add in the file ``.hg/hgrc`` something
  like::

    [paths]
    default = ssh://hg@bitbucket.org/paugier/fluidimage
    fluiddyn = ssh://hg@bitbucket.org/fluiddyn/fluidimage
    github = git+ssh://git@github.com/fluiddyn/fluidimage

  And in ``~/.hgrc``::

    [alias]
    update_master_github = !hg pull fluiddyn && hg up -r $(hg identify --id fluiddyn) && hg book master && hg book -i && hg push github -B master


A quite complicated example with hg-git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We open a PR::

  hg pull
  hg up master
  hg book fix/a_bug
  # Modify/add/remove files
  hg commit -m "A commit message"
  hg push -B fix/a_bug

We want to change something in the commit of the PR. We first try `hg absorb`.
Let's say that we are in a situation for which it does not work::

  # Modify/add/remove files
  hg commit -m "A different commit message" --amend
  # clean up Git commit map after history editing
  hg git-cleanup
  hg pull
  hg push -B fix/a_bug --force


Delete a bookmark in a remote repository (close a remote Git branch)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With Mercurial, `we can
do <https://stackoverflow.com/questions/6825355/how-do-i-delete-a-remote-bookmark-in-mercurial>`_::

  hg bookmark --delete <bookmark name>
  hg push --bookmark <bookmark name>

Unfortunately, it does not work for a remote Git repository (with hg-git).  We
have to use a Git client, clone the repository with Git and do `something like
<https://stackoverflow.com/a/10999165/1779806>`_::

  # this deletes the branch locally
  git branch --delete <branch name>
  # this deletes the branch in the remote repository
  git push origin --delete <branch name>
