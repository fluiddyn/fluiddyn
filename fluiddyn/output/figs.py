"""
Utilities for creating figures (:mod:`fluiddyn.output.figs`)
=============================================================

.. currentmodule:: fluiddyn.output.figs

Provides

.. autoclass:: Figure
   :members:

.. autoclass:: Figures
   :members:

"""


import os
import sys

import matplotlib
import matplotlib.pyplot as plt

from ..util import is_run_from_ipython
from .rcparams import set_rcparams


class Figures:
    """Represent a set of figures.

    Utilities to plot and save figures with matplotlib.

    Parameters
    ----------

    path_save : str
        Related to the path where to save.

    hastosave : bool
        If True, the function `Figure.saveifhasto` save the figure.

    for_beamer : bool
        If True, use beamer layout.

    for_article : bool
        If True, use article layout.

    fontsize : {18, int}
        Font size of the text in the figures.

    fontsize_pad : {9, int}
        Font size of the pad in the figures.
    """

    def __init__(
        self,
        path_save=None,
        hastosave=False,
        for_beamer=False,
        for_article=False,
        fontsize=18,
        fontsize_pad=9,
    ):

        self.hastosave = hastosave

        if path_save is None:
            self.path_save = os.getcwd()
        elif os.path.isabs(path_save):
            self.path_save = path_save
        else:
            self.path_save = os.path.join(os.getcwd(), path_save)

        set_rcparams(fontsize, for_article, for_beamer, fontsize_pad=9)

    def new_figure(
        self,
        name_file=None,
        num=None,
        fig_width_mm=200,
        fig_height_mm=150,
        size_axe=None,
    ):
        """Create a new Figure object and return it.

        Parameters
        ----------
        num : int, optional
            Number.

        fig_width_mm : {200, number}, optional
            Width (in mm)

        fig_height_mm : {150, number}, optional
            Height (in mm)

        size_axe : list, optional
            Size of the axe.

        name_file : str, optional
            Name of the file.

        """

        one_inch_in_mm = 25.4
        fig_width_inches = float(fig_width_mm) / one_inch_in_mm
        fig_height_inches = float(fig_height_mm) / one_inch_in_mm
        figsize = [fig_width_inches, fig_height_inches]

        dpi_latex = 72.27

        fig = Figure(
            num=num,
            figsize=figsize,
            dpi=dpi_latex,
            size_axe=size_axe,
            name_file=name_file,
            figures=self,
        )

        return fig


def show(block=None):
    """Show slightly more cleaver than old version of plt.show."""

    if block is None:
        if is_run_from_ipython():
            block = False
            plt.ion()
        else:
            block = True
            plt.ioff()

    if sys.platform.startswith("win") and not block:
        print("Warning: bug with anaconda and non-blocking show (?)")

    try:
        plt.show(block=block)
    except TypeError:
        plt.show()


class Figure(matplotlib.figure.Figure):
    """One figure.

    Improvement (?) of `matplotlib.figure.Figure`

    Parameters
    ----------
    (for the __init__ method)

    size_axe : list, optional
        Size of the axe.

    name_file : str, optional
        Name of the file.

    figures : :class:`fluiddyn.output.figs.Figures`
        Set of figures.

    kwargs : keyword arguments
        Given when create the figure.

    """

    def __init__(
        self, size_axe=None, name_file=None, figures=None, **kwargs  # *args,
    ):

        # Ugly workaround to be able to use the function plt.figure
        fig = plt.figure(**kwargs)
        for k, v in fig.__dict__.items():
            self.__dict__[k] = v

        if name_file is not None:
            self.name_file = name_file

        if figures is None:
            self.hastosave = True
            self.path_save = os.getcwd()
        else:
            self.hastosave = figures.hastosave
            self.path_save = figures.path_save
            self.figures = figures

        title = "Fig " + str(self.number)
        if name_file is not None:
            fig.name_file = name_file
            title += " " + name_file

        self.clf()
        self.canvas.manager.set_window_title(title)

        if size_axe is not None:
            self.add_axes(size_axe)

    def saveifhasto(self, name_file=None, hastosave=None, verbose=True):
        """Save the figure if `hastosave` is True.

        Parameters
        ----------

        name_file : str, optional
            Name of the file (the extension has to indicate the format).

        hastosave : bool, optional
            If True, save the figure.

        verbose : {True, bool}, optional
             Print nothing if False.

        """

        if hastosave is None:
            hastosave = self.hastosave

        if hastosave:

            if name_file is None:
                try:
                    name_file = self.name_file
                except AttributeError:
                    raise ValueError("No name given...")

            if not os.path.exists(self.path_save):
                os.mkdir(self.path_save)

            path = os.path.join(self.path_save, name_file)

            if verbose:
                print("Save figure in file\n" + path)

            super().savefig(path)
