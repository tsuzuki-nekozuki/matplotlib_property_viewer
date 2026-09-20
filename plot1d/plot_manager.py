from dataclasses import dataclass, field

from plot1d.plot_data import PlotData
from plot1d.plot_defaults import (
    default_colors, default_line_style, default_line_width,
    default_marker_size, default_marker_style
)
from plot1d.plot_generator import PlotGenerator
from plot1d.plot_settings import PlotSettings


class PlotManager:
    def __init__(self):
        self.min_nplots: int = 1
        self.max_nplots: int = 6
        self.default_marker_style: str = default_marker_style
        self.default_marker_size: float = default_marker_size
        self.default_line_style: str = default_line_style
        self.default_line_width: float = default_line_width
        self.default_colors: list = default_colors[:self.max_nplots]
        self.prefix: str = 'plot'
        self.settings: PlotSettings = PlotSettings()
        self.data: PlotData = PlotData()
        self.code: PlotGenerator = PlotGenerator(self.settings)
        self.add_plot()

    @property
    def nplots(self):
        return self.settings.nplots

    @property
    def plot_names(self):
        return self.settings.plot_names

    def add_plot(self):
        if self.nplots == self.max_nplots:
            return False
        pid = self.nplots
        name = f'{self.prefix}{self.nplots + 1}'
        self.settings.add_plot(
            name=name,
            line_style=self.default_line_style,
            line_width=self.default_line_width,
            line_color=self.default_colors[pid],
            marker_style=self.default_marker_style,
            marker_size=self.default_marker_size,
            marker_color=self.default_colors[pid]
        )
        self.data.add_data(is_random=True, offset=self.nplots)
        return True

    def delete_plot(self):
        if self.nplots == self.min_nplots:
            return False
        self.settings.delete_plot()
        self.data.delete_data()
        return True

    def get_plot(self, pid: int):
        return self.settings.plots[pid]

    def get_data(self, pid: int):
        return self.data.get_plot_data(pid).x, self.data.get_plot_data(pid).y

    def get_xdata(self, pid: int):
        return self.data.get_plot_data(pid).x

    def get_ydata(self, pid: int):
        return self.data.get_plot_data(pid).y

    def need_twin_axes(self):
        if not self.settings.has_twin_axes:
            return False
        if all(ip.yaxis == 0 for ip in self.settings.plots):
            return False
        return True

    def normalize(self):
        if self.settings.has_twin_axes and self.nplots == 1:
            self.settings.plots[0].yaxis = 0

        if not self.settings.has_twin_axes:
            for ip in self.settings.plots:
                ip.yaxis = 0

    def set_title_settings(self, item: str, value: str):
        match item:
            case 'title':
                self.settings.title = value
            case 'x':
                self.settings.label_xaxis = value
            case 'y':
                self.settings.label_yaxis = value
            case 'y2':
                self.settings.label_yaxis2 = value
            case _:
                raise ValueError(f'Unknown plot setting: {item}')

    def get_title_settings(self, item: str):
        match item:
            case 'title':
                return self.settings.title
            case 'x':
                return self.settings.label_xaxis
            case 'y':
                return self.settings.label_yaxis
            case 'y2':
                return self.settings.label_yaxis2
            case _:
                raise ValueError(f'Unknown plot setting: {item}')

    def enable_twinx(self, state: bool):
        self.settings.has_twin_axes = state

    def get_twin_axes_state(self):
        return self.settings.has_twin_axes

    def enable_grid(self, state: bool):
        self.settings.has_grid = state

    def get_grid_state(self):
        return self.settings.has_grid

    def enable_logscale(self, axis: str, state: bool):
        state = bool(state)
        match axis:
            case 'x':
                self.settings.is_xlog = state
            case 'y':
                self.settings.is_y1log = state
            case 'y2':
                self.settings.is_y2log = state
            case _:
                raise ValueError(f'Unknown plot setting: {axis}')

    def get_logscale_state(self, axis: str):
        match axis:
            case 'x':
                return self.settings.is_xlog
            case 'y':
                return self.settings.is_y1log
            case 'y2':
                return self.settings.is_y2log
            case _:
                raise ValueError(f'Unknown plot setting: {axis}')

    def update_plot_setting(
            self, pid: int, item: str, value: str | int | float):
        plot = self.settings.plots[pid]
        match item:
            case 'name':
                plot.name = value
            case 'line_width':
                plot.line_width = value
            case 'line_style':
                plot.line_style = value
            case 'marker_size':
                plot.marker_size = value
            case 'marker_style':
                plot.marker_style = value
            case 'marker_color':
                plot.marker_color = value
            case 'line_color':
                plot.line_color = value
            case 'y2':
                plot.yaxis = value
            case _:
                raise ValueError(f'Unknown plot setting: {item}')

    def get_plot_setting(self, pid: int, item: str):
        plot = self.settings.plots[pid]
        match item:
            case 'name':
                return plot.name
            case 'line_width':
                return plot.line_width
            case 'line_style':
                return plot.line_style
            case 'marker_size':
                return plot.marker_size
            case 'marker_style':
                return plot.marker_style
            case 'marker_color':
                return plot.marker_color
            case 'line_color':
                return plot.line_color
            case 'y2':
                return plot.yaxis
            case 'kwargs':
                return plot.plot_kwargs()
            case _:
                raise ValueError(f'Unknown plot setting: {item}')

    def generate_code(self):
        return self.code.generate()
