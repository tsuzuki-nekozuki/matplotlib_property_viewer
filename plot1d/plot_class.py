from dataclasses import dataclass, field
from typing import ClassVar

import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np

from numpy.typing import NDArray


@dataclass
class PlotSettings:
    default_colors: ClassVar[list[str]] = list(mc.TABLEAU_COLORS.keys())[:6]
    id: int = field(init=True)
    name: str = field(init=True)
    yaxis: int = field(init=False, default=0)
    marker_style: str = field(init=False, default='None')
    marker_size: float = field(
        init=False, default=plt.rcParams['lines.markersize'])
    marker_color: str = field(init=False)
    line_style: str = field(
        init=False, default=plt.rcParams['lines.linestyle'])
    line_width: float = field(
        init=False, default=plt.rcParams['lines.linewidth'])
    line_color: str = field(init=False)
    x: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))
    y: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))

    def __post_init__(self):
        self.marker_color = self.default_colors[self.id]
        self.line_color = self.default_colors[self.id]
        self.x = np.arange(100)
        self.y = np.random.rand(100) + (self.id + 1)

    def is_default_marker_style(self):
        return self.marker_style == 'None'

    def is_default_marker_color(self):
        return self.marker_color == self.default_colors[self.id]

    def is_default_marker_size(self):
        return self.marker_size == plt.rcParams['lines.markersize']

    def is_default_line_style(self):
        return self.line_style == plt.rcParams['lines.linestyle']

    def is_default_line_color(self):
        return self.line_color == self.default_colors[self.id]

    def is_default_line_width(self):
        return self.line_width == plt.rcParams['lines.linewidth']

    def is_base_color(self, color):
        return color in mc.BASE_COLORS.keys()

    def has_same_base_color(self):
        if self.marker_color != self.line_color:
            return False
        if not self.marker_color in mc.BASE_COLORS.keys():
            return False
        if self.marker_style == 'None' or self.marker_size == 0:
            return False
        if self.line_style == 'None' or self.line_width == 0:
            return False
        return True

    def plot_kwargs(self):
        return {
            'marker': self.marker_style,
            'ms': self.marker_size,
            'mec': self.marker_color,
            'mfc': self.marker_color,
            'ls': self.line_style,
            'lw': self.line_width,
            'c': self.line_color,
        }


@dataclass
class PlotManager:
    min_nplots: int = 1
    max_nplots: int = 6
    prefix: str = 'plot'
    plots: list[PlotSettings] = field(init=False, default_factory=list)
    title: str = field(init=False, default='')
    label_xaxis: str = field(init=False, default='')
    label_yaxis: str = field(init=False, default='')
    label_yaxis2: str = field(init=False, default='')
    has_grid: bool = field(init=False, default=False)
    has_twin_axes: bool = field(init=False, default=False)
    is_xlog: bool = field(init=False, default=False)
    is_y1log: bool = field(init=False, default=False)
    is_y2log: bool = field(init=False, default=False)

    def __post_init__(self):
        self.plots.append(PlotSettings(id=0, name='plot1'))

    @property
    def plot_names(self):
        return [i.name for i in self.plots]

    @property
    def nplots(self):
        return len(self.plots)

    def need_two_axes(self):
        if not self.has_twin_axes:
            return False
        if all([i.yaxis == 0 for i in self.plots]):
            return False
        return True

    def add_plot(self):
        if self.nplots == self.max_nplots:
            return False
        new_id = self.nplots
        new_plot = f'{self.prefix}{self.nplots + 1}'
        self.plots.append(PlotSettings(id=new_id, name=new_plot))
        return True

    def delete_plot(self):
        if self.nplots == self.min_nplots:
            return False
        del self.plots[-1]
        return True

    def normalize(self):
        if self.has_twin_axes and self.nplots == 1:
            self.plots[0].yaxis = 0

        if not self.has_twin_axes:
            for ip in self.plots:
                ip.yaxis = 0
