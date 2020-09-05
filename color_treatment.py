"""
Color Treatment
    Code to treat the color shenanigans

"""

# Extended Python #
import webcolors

# Some CSS21 colors don't work on the lamp, so translate them to something else.
# If it isn't in the table, we can pass it along no change.
COLOR_TRANSLATION = {"black": "white", "navy": "blue"}

COLOR_SPACE = webcolors.CSS21_HEX_TO_NAMES.items()
COLOR_BASE = tuple((*webcolors.hex_to_rgb(k),n) for k,n in COLOR_SPACE)


def closest_color(requested_color):
    """
    Get the closest color from the one provided.
    :param requested_color: <tuple> R,G,B
    :return color: <string>
    """

    min_colors = {}

    for r_c, g_c, b_c, name in COLOR_BASE:
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name

    return min_colors[min(min_colors.keys())]


def get_color_name(requested_color):
    """
    Get a name for the given color.
    :param requested_color: <tuple> R,G,B
    :return best_name
    """

    try:
        best_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        best_name = closest_color(requested_color)

    if best_name in COLOR_TRANSLATION:
        best_name = COLOR_TRANSLATION[best_name]

    return best_name
