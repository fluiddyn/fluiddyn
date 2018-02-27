Automated workflow for developers
=================================

Since various specialized packages are hosted under decentralized repositories
(repos) in the FluidDyn project, which can be frequently updated, it can become
*overwhelming* to clone each of these one-by-one or to go into every directory
and run ``hg pull -u`` as a routine. Instead you can use `fluiddevops
<https://pypi.org/project/fluiddevops/`_ designed for this exact purpose. To
get started::

  pip install fluiddevops
  wget https://bitbucket.org/fluiddyn/fluiddevops/raw/default/examples/mirror.cfg

The package ``fluiddevops`` provides the console utility ``fluidmirror`` which
can perform clone, pull, push with multiple repositories::

  $ fluidmirror -h
  usage: fluidmirror [-h] [-c CFG] {list,clone,set-remote,pull,push,sync} ...

  works on a specific / all configured repositories (default)

  positional arguments:
    {list,clone,set-remote,pull,push,sync}
                          sub-command
      list                list configuration
      clone               hg clone
      set-remote          set remote (push) path in hgrc
      pull                hg pull -u
      push                hg push
      sync                sync: pull and push

  optional arguments:
    -h, --help            show this help message and exit
    -c CFG, --cfg CFG     config file

Let us clone all the FluidDyn repos!::

  fluidmirror clone

Pull all recent commits and update, for daily use (since cloning is done only once)::

  fluidmirror pull


How it works
------------
You would have a configuration file ``mirror.cfg`` which looks like this::

  [defaults]
  pull_base = https://bitbucket.org/fluiddyn
  push_base = ssh://hg@bitbucket.org/fluiddyn
  ssh = ssh -oStrictHostKeyChecking=no

  [repo:fluiddyn]
  pull =
  push =

  [repo:fluidsim]
  pull =
  push =

  [repo:fluidlab]
  pull =
  push =

  [repo:fluidimage]
  pull =
  push =

  [repo:fluidfft]
  pull =
  push =

See how the configuration is interpreted::

  $ fluidmirror list
  repo: fluiddyn
  pull: https://bitbucket.org/fluiddyn/fluiddyn
  push: ssh://hg@bitbucket.org/fluiddyn/fluiddyn

  repo: fluidsim
  pull: https://bitbucket.org/fluiddyn/fluidsim
  push: ssh://hg@bitbucket.org/fluiddyn/fluidsim

  repo: fluidlab
  pull: https://bitbucket.org/fluiddyn/fluidlab
  push: ssh://hg@bitbucket.org/fluiddyn/fluidlab

  repo: fluidimage
  pull: https://bitbucket.org/fluiddyn/fluidimage
  push: ssh://hg@bitbucket.org/fluiddyn/fluidimage

  repo: fluidfft
  pull: https://bitbucket.org/fluiddyn/fluidfft
  push: ssh://hg@bitbucket.org/fluiddyn/fluidfft

The ``defaults`` section describes the base URLs to pull from and push to. For
example, for the repo ``fluiddyn`` the pull URL will be
``join(pull_base,repo)`` which would be
``https://bitbucket.org/fluiddyn/fluiddyn``.


Customizing
-----------
You can add more sections to or customize the configuration as you prefer.

Any non-empty value added under a ``repo:`` section would override the
defaults. For example, let's add a new repo and override the default pull &
push URLs as follows::

  [repo:pythran]
  pull = https://github.com/serge-sans-paille/pythran
  push = https://github.com/fluiddyn/pythran
