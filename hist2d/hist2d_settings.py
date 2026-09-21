from dataclasses import dataclass, field

from hist2d.hist2d_defaults import default_cmap


@dataclass
class Hist2dSettings:
    xmin: float = field(init=False, default=-100)
    xmax: float = field(init=False, default=100)
    xbin_count: int = field(init=False, default=20)
    ymin: float = field(init=False, default=-100)
    ymax: float = field(init=False, default=100)
    ybin_count: int = field(init=False, default=20)
    colormap: str = field(init=False, default=default_cmap)
    title: str = field(init=False, default='')
    label_xaxis: str = field(init=False, default='')
    label_yaxis: str = field(init=False, default='')
    is_zlog: bool = field(init=False, default=False)
    has_colorbar: bool = field(init=False, default=False)
