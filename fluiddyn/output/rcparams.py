"""
Default parameters for Matplotlib figures
=========================================

.. currentmodule:: fluiddyn.output.rcparams

"""

import matplotlib.pyplot as plt


def set_rcparams(fontsize=18, for_article=True, for_beamer=False):

    if for_article or for_beamer:
        params = {
            # 'backend': 'ps',
            'axes.labelsize': fontsize,
            'font.size': fontsize,
            'legend.fontsize': fontsize,
            'axes.titlesize': fontsize,
            'xtick.labelsize': fontsize,
            'ytick.labelsize': fontsize,
            'xtick.major.pad': 9,
            'xtick.major.pad': 9,
            'text.usetex': True,
            'font.family': 'serif',
            'font.serif': 'Computer Modern Roman',
            'font.sans-serif': 'Computer Modern Roman',
            'ps.usedistiller': 'xpdf'}

    if for_beamer:
        params['font.family'] = 'sans-serif'
        preamble = r'''\usepackage[cm]{sfmath}'''
        plt.rc('text.latex', preamble=preamble)

    if for_article or for_beamer:
        plt.rcParams.update(params)
