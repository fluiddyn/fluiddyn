FROM python:3.8-bullseye
LABEL Pierre Augier <pierre.augier@univ-grenoble-alpes.fr>

COPY docker/hgrc $HOME/.hgrc

RUN apt-get update

RUN apt-get install -y --no-install-recommends emacs vim rsync python3-pip
RUN apt-get install -y --no-install-recommends mercurial git
RUN apt-get install -y --no-install-recommends libopenmpi-dev

RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p $HOME/.config/matplotlib
RUN echo 'backend      : agg' > $HOME/.config/matplotlib/matplotlibrc

RUN /usr/bin/python3 -m pip install hg-git hg-evolve
RUN git config --global pull.rebase false

RUN /usr/bin/python3 -m pip install pip tox black isort -U