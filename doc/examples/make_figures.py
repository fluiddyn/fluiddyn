import os

import numpy as np

from fluiddyn.output.figs import Figures, show

path = "/tmp/example_figs_fluiddyn"

if not os.path.exists(path):
    os.makedirs(path)

figures = Figures(path, hastosave=True, for_article=True)

fig = figures.new_figure("figure0.png")
ax = fig.gca()

x = np.linspace(0, 2, 10)
ax.plot(x, x ** 2)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$\Pi / \varepsilon$")

fig.saveifhasto()


fig = figures.new_figure("figure1.pdf")
ax = fig.gca()

x = np.linspace(-2, 2, 10)
ax.plot(x, x ** 3, "r--")

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$C_2(x)$")

fig.saveifhasto()


show()
