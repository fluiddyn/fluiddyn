"""Utilities for creating movies (:mod:`fluiddyn.output.movies`)
===============================================================

.. warning::

   Don't use this file. Now movies can be made with matplotlib.animation.

Provides

.. autosummary::
   :toctree:

   MoviesFromData


Warning: this file is a little bit buggy because the memory is not
released when figures are not plotted. Also it is much too slow for
real time movies. These problems have to be solved!

"""
from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt

import os

import gc

from glob import glob

from fluiddyn.io.hdf5 import H5File
# from fluiddyn.util.timer import Timer
import fluiddyn.output.figs as figs


class MoviesFromData:
    """A class for creating movies."""

    def __init__(self, path_dir=None,
                 name_file_generic='state_phys*.hd5'):
        self.set_fps(12.)

        if path_dir is None:
            path_dir = os.getcwd()
        self.path_dir = path_dir

        self.files = glob(
            os.path.join(self.path_dir, name_file_generic))

        self.files.sort()

        with H5File(self.files[0]) as f:
            p = f['param']
            self.Lx = p['Lx'][...]
            self.Ly = p['Ly'][...]
            eta = f['state_phys']['eta'][...]
            self.nx = eta.shape[1]
            self.ny = eta.shape[0]

        P0 = 1
        Lh = 50.
        deltak = 2*np.pi/Lh
        kf = 6*deltak
        self.Lf = np.pi/kf
        self.Tf = (P0 * kf**2)**(-1/3)
        print('kf, Lf, Tf:', kf, self.Lf, self.Tf)

        self.x = self.Lx/self.nx * np.arange(self.nx)/self.Lf
        self.y = self.Ly/self.ny * np.arange(self.ny)/self.Lf

        self.param_movie = {
            'itlim': [0, len(self.files)-1],
            'xlim': [0, self.Lx],
            'ylim': [0, self.Ly],
            'fig_width_mm': 240,
            'fig_height_mm': 200,
            'size_axe': [0.11, 0.11, 0.88, 0.81],
            'vmax': eta.max()}

    def get_frame(self, i):
        with H5File(self.files[i]) as f:
            data = f['Obj_state_phys']['eta'][...]
            tframe = f['Obj_state_phys'].attrs['time']
            return data, tframe

    def plot_one_frame(self, ax, field, tframe):
        # ax.clear()
        vmax = self.param_movie['vmax']
        # plt.gcf().text_time.set_text(
        #     '$t/T_f = {:6.2f}$'.format(tframe/self.Tf))
        ax.lines = []
        pc = ax.pcolormesh(
            self.x, self.y, 1+field,
            vmin=1-self.param_movie['vmax'], vmax=1+self.param_movie['vmax'])
        return pc

    def prepare_fig(self, it=0):

        pm = self.param_movie

        fig = self.figures.new_figure(
            fig_width_mm=pm['fig_width_mm'],
            fig_height_mm=pm['fig_height_mm'],
            size_axe=pm['size_axe'],
            name_file='movie')
        ax = plt.gca()

        ax.set_xlabel('$x/L_f$')
        ax.set_ylabel('$y/L_f$')

        field, tframe = self.get_frame(it)

        if not hasattr(fig, 'text_time'):
            fig.text_time = ax.text(
                5., 12.3, '$t/T_f = {:6.2f}$'.format(tframe/self.Tf),
                fontsize=20)
            ax.text(13.2, -1., '$h$', fontsize=24)

        pc = self.plot_one_frame(ax, field, tframe)

        plt.colorbar(pc)

        return fig, ax

    def set_xlim(self, xlim):
        self.xlim = xlim

    def set_ylim(self, ylim):
        self.ylim = ylim

    def set_fps(self, fps):
        self.fps = fps

    def play_movie(self, **kwargs):

        for k, v in kwargs.items():
            self.param_movie[k] = v

        self.figures = figs.Figures(
            for_beamer=True,
            path_save=os.path.join(self.path_dir, 'Images'),
            hastosave=False)

        plt.ion()

        pm = self.param_movie

        itlim = pm['itlim']

        fig, ax = self.prepare_fig(itlim[0])

        # timer = Timer(1/self.fps)
        for it in range(itlim[0], itlim[1]):
            field, tframe = self.get_frame(it)
            self.plot_one_frame(ax, field, tframe)
            plt.draw()
            # timer.wait_tick()

    def save_images(self, **kwargs):

        for k, v in kwargs.items():
            self.param_movie[k] = v

        self.figures = figs.Figures(
            for_beamer=True,
            path_save=os.path.join(self.path_dir, 'Images'),
            hastosave=True)

        plt.ioff()

        itlim = self.param_movie['itlim']
        for it in range(itlim[0], itlim[1]):
            fig, ax = self.prepare_fig(it=it)
            # field, tframe = self.get_frame(it)
            # self.plot_one_frame(ax, field, tframe)
            fig.saveifhasto(name_file='im{:05d}'.format(it), format='png')
            plt.close(fig)
            gc.collect()

    def save_movie_from_images(self, ):
        pass

    command = """
mencoder 'mf://im*.png' -mf type=png:fps=8 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o movie.mpg
"""


if __name__ == '__main__':
    path_dir = (
'/data/reasons/pa371/Temp'
'/SE2D_SW1lwaves_forcingw_L=50.x50._960x960_c=20_f=0_2014-07-14_13-44-35'
# '/SE2D_SW1lwaves_forcingw_L=50.x50._960x960_c=20_f=0_2014-07-14_10-10-08'
)

    m = MoviesFromData(path_dir)
