"""Helper to choose RGB sets of colors for figures
==================================================

Provides

.. autofunction:: make_pdf_colorchart

"""

from __future__ import division

from colorsys import hsv_to_rgb

import subprocess
import os
import shlex


def make_pdf_colorchart(nb_colors=4, darkest_gray=0.03,
                        lightest_gray=0.85):
    """Produce a pdf with color charts.

    The color charts help choosing RGB sets of colors which are
    distinguishable both in black and white and in color.

    Notes
    -----

    For many journals, it is very expensive to have figures with
    colors in the printed version. But nowadays, the printed version
    of a paper is not very important because most people get numerical
    papers on the web. So a good solution for many figures is to use
    colors that can be differentiated in black and white. This
    function produces pdf files with color charts helping researchers
    to choose colors adapted to this requirement.

    Warning: the command pdflatex and the Latex package Tikz are used
    to produce the final document.

    First author: Tobit CAUDWELL 2015 (tobit [AT] locta.fr).

    Parameters
    ----------

    nb_colors : int
        nb of desired final colors.

    darkest_gray : float
        darkest gray level (between 0 and 1)

    lightest_gray : float
        lightest gray level (between 0 and 1)

    """

    colors = []
    nbHue = 30  # nb of  hue values
    nbSV = 200  # nb of light/dark nuances

    # Creation of a table with colors sorted according to their hue
    for h in range(nbHue+1):
        for sv in range(nbSV+1):
            # variations along s
            RGBcolor = hsv_to_rgb(h/nbHue, sv/nbSV, 1)
            # multiply RGBcolor by 255
            RGBcolor = tuple(i*255 for i in RGBcolor)

            luminance = (0.2126*RGBcolor[0] + 0.7152*RGBcolor[1] +
                         0.0722*RGBcolor[2])
            colors.append([h, RGBcolor, luminance])

            # variations along v
            RGBcolor = hsv_to_rgb(h/nbHue, 1, sv/nbSV)
            # multiply RGBcolor by 255
            RGBcolor = tuple(i*255 for i in RGBcolor)

            luminance = (0.2126*RGBcolor[0] + 0.7152*RGBcolor[1] +
                         0.0722*RGBcolor[2])
            colors.append([h, RGBcolor, luminance])

    # round of luminance values
    lumRnd = 2.
    nbGray = int(round(256.0/lumRnd))
    # list of list where color are sorted
    color_table = [[0 for i in range(nbHue)] for j in range(nbGray)]
    for l in colors:
        h = l[0]
        luminance = l[2]
        # Position in color_table
        idx_lum = int(round(luminance/lumRnd)) - 1
        # First dim = luminance, 2nd dim = HUE
        color_table[idx_lum][h-1] = l

    darkest_gray = darkest_gray*255
    lightest_gray = lightest_gray*255
    gray_wanted = [lightest_gray + i*(darkest_gray-lightest_gray)/(nb_colors-1)
                   for i in range(nb_colors)]  # equivalent to linspace
    # index of desired list in color_table
    idx = [int(round(x/lumRnd)) for x in gray_wanted]

    # Selection of final colors
    final_colors = []
    for i in idx:
        colors = [x[1] for x in color_table[i]]
        final_colors.append(colors)

    # create the text of the latex file
    lines = [(
        r"""\documentclass{standalone}
\usepackage{tikz,calc}
\begin{document} \small
\begin{tikzpicture}""")]

    x = 0
    for line in reversed(final_colors):
        y = 0
        for col in line:
            coltxt = str([round(i/255, 2) for i in col])
            lines.append(
                r'\definecolor{currentcolor}{rgb}{' +
                coltxt[1:-1] + '}\n'
                r'\node[fill=currentcolor, '
                'minimum width=3cm, minimum height=1cm] at (' +
                str(x) + "," + str(y) + r') {' + coltxt + '};')
            y -= 1
        x += 3.5

    x = 0
    for g in reversed(gray_wanted):
        coltxt = str([round(g/255, 2) for i in range(3)])
        lines.append(
            r'\definecolor{currentcolor}{rgb}{' +
            coltxt[1:-1] + '}\n'
            r'\node[fill=currentcolor, minimum width=3cm, '
            'minimum height=1cm] at (' +
            str(x) + r',2) {' + coltxt + '};')
        x += 3.5

        lines.append(r'\end{tikzpicture}' + '\n' + r'\end{document}')

    # write the .tex file
    file_name = "colorchart_using_" + str(nb_colors) + "_levels"
    with open(file_name + ".tex", "w") as f:
        f.write('\n'.join(lines))

    # PdfLaTeX compilation for PDF output
    proc = subprocess.Popen(shlex.split('pdflatex ' + file_name + ".tex"))
    proc.communicate()

    # delete .tex .log and .aux
    os.unlink(file_name + ".tex")
    os.unlink(file_name + ".log")
    os.unlink(file_name + ".aux")

    print('Document ' + file_name + '.pdf written.')


if __name__ == '__main__':
    make_pdf_colorchart(nb_colors=4, darkest_gray=0.5, lightest_gray=0.85)
