FROM python:3.11
LABEL Pierre Augier <pierre.augier@univ-grenoble-alpes.fr>
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update
RUN apt-get install -y --no-install-recommends emacs vim rsync git
RUN apt-get install -y --no-install-recommends libopenmpi-dev libfftw3-dev

RUN rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 appuser && useradd -m -r -u 1000 -g appuser -s /bin/bash appuser -s /bin/bash && usermod -a -G sudo appuser
RUN echo appuser:appuser | chpasswd
USER appuser
ARG HOME=/home/appuser
RUN mkdir -p $HOME/opt
WORKDIR $HOME/opt
RUN echo $USER $HOME $PWD && whoami

COPY docker/hgrc $HOME/.hgrc
RUN mkdir -p $HOME/.local/bin
ENV PATH=$HOME/.local/bin:$PATH

RUN mkdir -p $HOME/.config/matplotlib
RUN echo 'backend      : agg' > $HOME/.config/matplotlib/matplotlibrc

RUN git config --global pull.rebase false

RUN uv tool install mercurial --with hg-evolve,hg-git
RUN uv tool install pdm
RUN uv tool install nox
RUN uv tool install isort
RUN uv tool install black
RUN uv tool install vermin
