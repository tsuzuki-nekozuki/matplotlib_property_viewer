from dataclasses import dataclass, field


@dataclass
class OnePlotSettings:
    name: str
    line_style: str
    line_width: float
    line_color: str
    marker_style: str
    marker_size: float
    marker_color: str
    yaxis: int = 0

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
class PlotSettings:
    plots: list[OnePlotSettings] = field(init=False, default_factory=list)
    title: str = field(init=False, default='')
    label_xaxis: str = field(init=False, default='')
    label_yaxis: str = field(init=False, default='')
    label_yaxis2: str = field(init=False, default='')
    has_grid: bool = field(init=False, default=False)
    has_twin_axes: bool = field(init=False, default=False)
    is_xlog: bool = field(init=False, default=False)
    is_y1log: bool = field(init=False, default=False)
    is_y2log: bool = field(init=False, default=False)

    @property
    def nplots(self):
        return len(self.plots)

    @property
    def plot_names(self):
        return [ip.name for ip in self.plots]

    def add_plot(
        self,
        name: str,
        line_style: str,
        line_width: float,
        line_color: str,
        marker_style: str,
        marker_size: float,
        marker_color: str
    ):
        new_plot = OnePlotSettings(
            name=name,
            line_style=line_style,
            line_width=line_width,
            line_color=line_color,
            marker_style=marker_style,
            marker_size=marker_size,
            marker_color=marker_color,
        )
        self.plots.append(new_plot)

    def delete_plot(self):
        del self.plots[-1]
