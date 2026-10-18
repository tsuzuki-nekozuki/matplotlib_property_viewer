from dataclasses import dataclass, field


@dataclass
class OneScatterSettings:
    name: str
    scatter_type: str
    style: str
    alpha: float
    color1: str
    color2: str
    edge: float
    scatter_size: float
    bubble_size: float
    width: float
    colormap: str
    vmin: float
    vmax: float


@dataclass
class ScatterSettings:
    plots: list[OneScatterSettings] = field(init=False, default_factory=list)
    xmin: float = field(init=False, default=-100)
    xmax: float = field(init=False, default=100)
    ymin: float = field(init=False, default=-100)
    ymax: float = field(init=False, default=100)
    title: str = field(init=False, default='')
    label_xaxis: str = field(init=False, default='')
    label_yaxis: str = field(init=False, default='')
    is_xlog: bool = field(init=False, default=False)
    is_ylog: bool = field(init=False, default=False)
    has_grid: bool = field(init=False, default=False)

    def set_nplots(self, n: int):
        self.plots = [OneScatterSettings] * n
