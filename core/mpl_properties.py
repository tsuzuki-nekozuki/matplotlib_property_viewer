import matplotlib.lines as ml
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib.font_manager as fm


def get_color_list():
    tableau = mc.TABLEAU_COLORS
    base = mc.BASE_COLORS
    css4 = mc.CSS4_COLORS
    colors = ['- TABLEAU COLORS -'] + list(tableau.keys())
    colors.extend(['- BASE COLORS -'] + list(base.keys()))
    colors.extend(['- CSS4 COLORS -'] + list(css4.keys()))
    return colors


def get_marker_list():
    markers = ['None'] + [f'{k}' for k in ml.Line2D.markers.keys()]
    return markers


def get_line_list():
    return ['None', 'solid', 'dashed', 'dotted', 'dashdot']


def get_colormap_list():
    return plt.colormaps()


def get_fonts_list():
    ttf = set([f.name for f in fm.fontManager.ttflist])
    # afm = set([f.name for f in fm.fontManager.afmlist])
    return list(ttf)
