# A workflow to produce figures for articles and thesis

I (Pierre Augier) describe in this page a workflow to produce figures for
articles and thesis. This workflow is adapted for studies for which
open-science can be used. After publication, everything (data and software) is
open. This workflow is perfectly adapted for studies using Fluidsim.

This workflow is based on the usage of a repository where all the source files
for the final document are included and versioned. Typically, it can be one
repository per PhD student or postdoc. Note that the data is usually not
included in this repository (a repository is adapted for source files). For an
article, the real life example
[2022strat_turb_toro](https://foss.heptapod.net/fluiddyn/fluiddyn_papers/-/tree/branch/default/2022strat_turb_toro)
in our repository fluiddyn_papers can be used as a template.

Except for particular cases (described below), the figures are not included in
the repository (not versioned) and are produced locally before the build of the
document (article or thesis) from a selection of data made public.

## Diagram on the workflow

```{mermaid}
  flowchart TD
    RawData[(Raw data\non lab disks)] -- Script .sh with rsync commands --> Selection[(Selected data\non lab disks)]
    Selection -- Dropbox like client --> Cloud[(Selected data on the cloud)]
    Cloud -- Dropbox like client --> SelectionLocal[(Selected data\non local disk)]
    SelectionLocal -- Script make_figures.py --> Figs[Figures and tables\nis a tmp directory]
```

### Raw data on lab disks

This can be simulation folders with Fluidsim data and results of post
processing. These are typically .txt, .nc or .h5 files. This raw data can be as
huge as necessary (typically some terabytes).

### Selected data on lab disks

We use Dropbox like open-source services based on OwnCloud
(<https://mycore.core-cloud.net>, provided by CNRS) or NextCloud
(<https://cloud.univ-grenoble-alpes.fr>, provided by UGA).

We need to restrict the selected data to a reasonable size (something like few
gigabytes).

One needs to think about how to select the data. It depends a lot on the study.
The goal is to select only what is necessary to produce the figures and the
tables. Of course, it can be very useful to produce also some extra figures
that won't be included in the article / thesis. It could also be useful to
include one notebook per simulation summarizing the physical results. We can
produce these notebooks and associated pdf with
[Papermill](https://papermill.readthedocs.io) and
[Nbconvert](https://nbconvert.readthedocs.io) (as in [this
example](https://foss.heptapod.net/fluiddyn/fluidsim/-/blob/branch/default/doc/examples/forcing_anisotropic_3d/toro2022/postrun640.py)).

When the article is accepted, this directory can be used to create a
[Zenodo](https://zenodo.org/) or [Figshare](https://figshare.com/) dataset. The
last version of the code used to produce the article can be included in the
dataset, so that it is very easy for anyone to reproduce the figures and play
with the data.

### Script .sh with rsync commands

The directory in the lab disks containing the selected data can be produced
with some `rsync` commands. This could be something like:

```bash
#!/usr/bin/env bash

PROJECT_DIR=$PROJECT_DIR
MyCore_DIR=...

rsync -aP \
  $PROJECT_DIR/results_papermill/* \
  $PROJECT_DIR/from_occigen/aniso/results_papermill/* \
  $MyCore_DIR/2022strat-turb-toro/notebooks

rsync -aP \
  $PROJECT_DIR/aniso/ns3d* \
  $PROJECT_DIR/from_occigen/aniso/ns3d* \
  $MyCore_DIR/2022strat-turb-toro/simul_folders \
  --exclude "**/spatiotemporal/rank*_tmin*.h5" \
  --exclude "**/state_phys_t*.h5" \
  --exclude "end_states/*" \
  --exclude "results_papermill/*" \
  --exclude "**/*_uncompressed.h5" \
  --exclude "*/State_phys_*"
```

Note that we could also use symbolic links but then we need to keep the raw
data.

### Production of the figures and tables with Python

The command `make` has to produce the final .pdf document. However, it seems
easier to call in the `Makefile` a Python script `py/make_figures.py` that
check what needs to be done to produce the figures.

```Makefile
NAME = article

$(NAME).pdf: figures
	cd input && latexmk -shell-escape -pdf $(NAME).tex && rsync $(NAME).pdf ../$(NAME).pdf

figures:
	python py/make_figures.py SAVE

clean:
	rm -f tmp/table.tex
	cd input && rm -f *.aux *.fdb_latexmk *.fls *.log *.bak* *.bbl *.blg *.out *Notes.bib

cleantmp:
	rm -rf tmp

cleanall: clean cleantmp
	rm -f *.pdf

format:
	cd input && formattex *.tex -i
```

Fluiddyn provides a function `fluiddyn.util.has_to_be_made` which is very
useful to write `py/make_figures.py`.

Note that other tools like [snakemake](https://snakemake.github.io/) and
[invoke](https://www.pyinvoke.org/) could be used to produce the figures, the
tables and the document.

## Special cases for figures

Some figures do not fit well into this workflow:

1. Some figures cannot be produced locally on the computer used to build the
   final document. This is for example the case of figures produced with Paraview
   from a huge data file.

1. Some sketches produced for example with Inkscape.

In this case, the images (.png or .eps) can be included in the repository of
the document source. Note that it is really better to also include in the
repository the "sources" of these images, for example .svg for Inkscape or
Python scripts for Paraview to ease potential modifications of the images.

## Tools to produce the final document

Once the figures and tables are created, the final step is to create the
document. Latex is still the de-facto document format for articles in fluid
mechanics.

It can be useful to avoid the Latex format for the text of the document. I was
quite happy with Pandoc for [this
paper](https://foss.heptapod.net/fluiddyn/fluiddyn_papers/-/tree/branch/default/reply_Zwart2020).

For a PhD thesis in 2022, I would recommend looking at
[Jupyterbook](https://jupyterbook.org/) and [MyST
Markdown](https://jupyterbook.org/en/stable/content/myst.html), but the
important thing is to find a good tool adapted to your needs. One good entry point to
find such tool can be [this very nice
guide](https://github.com/writing-resources/awesome-scientific-writing/).
