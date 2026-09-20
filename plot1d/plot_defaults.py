import matplotlib.colors as mc
import matplotlib.pyplot as plt

default_marker_style: str = plt.rcParams['lines.marker']
default_marker_size: float = plt.rcParams['lines.markersize']
default_line_style: str = plt.rcParams['lines.linestyle']
default_line_width: float = plt.rcParams['lines.linewidth']
default_colors: list = list(mc.TABLEAU_COLORS.keys())
