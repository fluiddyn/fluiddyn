"""
Default parameters for Matplotlib figures
=========================================

.. currentmodule:: fluiddyn.output.rcparams

"""

import matplotlib.pyplot as plt


def set_rcparams(fontsize=18, for_article=True, for_beamer=False,
                 fontsize_pad=9):

    params = {
        'axes.labelsize': fontsize,
        'font.size': fontsize,
        'legend.fontsize': fontsize,
        'axes.titlesize': fontsize,
        'xtick.labelsize': fontsize-2,
        'ytick.labelsize': fontsize-2,
        'xtick.major.pad': fontsize_pad,
        'xtick.major.pad': fontsize_pad}

    if for_article or for_beamer:
        params_tmp = {
            'text.usetex': True,
            'font.family': 'serif',
            'font.serif': 'Computer Modern Roman',
            'font.sans-serif': 'Computer Modern Roman',
            'ps.usedistiller': 'xpdf'}

        for k, v in list(params_tmp.items()):
            params[k] = v

    if for_beamer:
        params['font.family'] = 'sans-serif'
        preamble = r'''\usepackage[cm]{sfmath}'''
        plt.rc('text.latex', preamble=preamble)

    plt.rcParams.update(params)
