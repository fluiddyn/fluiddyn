(advicedev)=

# FluidDyn development

Discussions on the development of the FluidDyn packages take place in the
[FluidDyn developer chat room](https://riot.im/app/#/room/#fluiddyn-dev:matrix.org).

For FluidDyn, we use the revision control software Mercurial and our main repositories
are hosted here: <https://foss.heptapod.net/fluiddyn>.

[Heptapod](https://heptapod.net/) is a friendly fork of GitLab Community Edition
supporting Mercurial. <https://foss.heptapod.net> is a public instance for Free and
Open-Source Software (more information
[here](https://foss.heptapod.net/heptapod/foss.heptapod.net)).

Thanks to [Octobus](https://octobus.net/) and
[Clever Cloud](https://www.clever-cloud.com) for providing this service!

```{raw} html
<h1 align="center">
  <a href="https://foss.heptapod.net/heptapod/foss.heptapod.net">
    <img width="500" alt="Octobus + Clever Cloud"
         src="https://foss.heptapod.net/heptapod/slides/2020-FOSDEM/raw/branch/default/octobus+clever.png"
         >
  </a>
</h1>
```

If you are new with Mercurial and Heptapod, you should read
[our dedicated tutorial](https://fluidhowto.readthedocs.io/en/latest/mercurial.html)

```{warning}
We wrote a specific Mercurial extension for FluidDyn development called
[hg-fluiddyn](https://foss.heptapod.net/fluiddyn/hg-fluiddyn). All
FluidDyn contributors / developers / maintainers should install and activate
it! We explain [here](https://fluidhowto.readthedocs.io/en/latest/mercurial.html) how
to do that.
```

```{toctree}
---
maxdepth: 1
---
workflow_release
```

## Few important coding tips

- Always use a good Python editor! Indentation has to be handle automatically for you
  (you should never count the spaces) and you have to have tips from flake8. We use and
  recommend FOSS editors like Spyder, Visual Studio Code, Vim or Emacs. For the two last
  solutions, a good configuration is mandatory.
- Use the Python code formatter [black](https://github.com/psf/black) with the command
  `make black`.
- It is usually a good practice to run the unittests before committing (see the Makefile
  of each repositories).

## fluiddevops: a tool to handle the FluidDyn repositories (will be depreciated)

We present a tool to handle the different FluidDyn repositories.

```{toctree}
---
maxdepth: 1
---
workflow_dev
```
