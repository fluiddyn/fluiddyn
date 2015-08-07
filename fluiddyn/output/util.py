

def gradient_colors(nb_colors, color_start=None,
                    color_end=None):
    """Produce a color gradient."""
    if color_start is None:
        color_start = [1, 0, 0]
    if color_end is None:
        color_end = [0, 0, 1]
    # start at black, finish at white
    gradient = [color_start]
    # If only one color, return black
    if nb_colors == 1:
        return gradient
    # Calcuate a color at each evenly spaced value
    # of t = i / n from i in 0 to 1
    for t in range(1, nb_colors):
        gradient.append(
            [color_start[j]
             + (float(t)/(nb_colors-1))*(color_end[j]-color_start[j])
             for j in range(3)
             ])
    return gradient
