FROM python:3.9-bookworm
LABEL Pierre Augier <pierre.augier@univ-grenoble-alpes.fr>

COPY docker/hgrc $HOME/.hgrc

RUN apt-get update

RUN apt-get install -y --no-install-recommends emacs vim rsync python3-pip
RUN apt-get install -y --no-install-recommends mercurial git
RUN apt-get install -y --no-install-recommends libopenmpi-dev libfftw3-dev

RUN rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 appuser && useradd -m -r -u 1000 -g appuser -s /bin/bash appuser -s /bin/bash && usermod -a -G sudo appuser
RUN echo appuser:appuser | chpasswd
USER appuser
ARG HOME=/home/appuser
RUN mkdir -p $HOME/opt
WORKDIR $HOME/opt
RUN echo $USER $HOME $PWD && whoami

RUN mkdir -p $HOME/.local/bin
ENV PATH=$HOME/.local/bin:$PATH

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN mkdir -p $HOME/.config/matplotlib
RUN echo 'backend      : agg' > $HOME/.config/matplotlib/matplotlibrc

RUN $(hg debuginstall -T '{pythonexe}') -m pip install hg-evolve hg-git --no-cache-dir --user
RUN git config --global pull.rebase false

RUN python -m pip install pip nox pdm black isort vermin -U --user
