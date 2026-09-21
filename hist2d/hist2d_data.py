from dataclasses import dataclass, field

import numpy as np

from numpy.typing import NDArray


@dataclass
class Hist2dData:
    xmin: float = field(init=False, default=-100)
    xmax: float = field(init=False, default=100)
    ymin: float = field(init=False, default=-100)
    ymax: float = field(init=False, default=100)
    ndata: int = field(init=False, default=1000000)
    data: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))

    def __post_init__(self):
        self.generate()

    def generate(self, is_random: bool = True):
        if is_random:
            rng = np.random.default_rng()
            # 2D gaussian
            xhalf = (self.xmax - self.xmin) / 2.
            yhalf = (self.ymax - self.ymin) / 2.
            nx = rng.integers(1, 7)
            ny = rng.integers(1, 7)
            # Peak positions
            if nx == 1:
                xpeaks = np.array([0])
                xsigma = xhalf / 2
            else:
                xpeaks = np.linspace(- xhalf, xhalf, nx)
                xsigma = xhalf / (nx - 1) / 2
            if ny == 1:
                ypeaks = np.array([0])
                ysigma = yhalf / 2
            else:
                ypeaks = np.linspace(- yhalf, yhalf, ny)
                ysigma = yhalf / (ny - 1) / 2
            # Select peaks
            peak_indices = rng.integers(0, nx * ny, size=self.ndata)
            ix, iy = divmod(peak_indices, ny)
            # Generate samples
            px = rng.normal(loc=xpeaks[ix], scale=xsigma)
            py = rng.normal(loc=ypeaks[iy], scale=ysigma)
            px = px + (self.xmax + self.xmin) / 2.
            py = py + (self.ymax + self.ymin) / 2.
            self.data = np.array([px, py]).swapaxes(0, 1)
