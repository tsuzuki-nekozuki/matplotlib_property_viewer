from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np

from numpy.typing import NDArray


@dataclass
class Hist2dSettings:
    xmin: float = field(init=False, default=-100)
    xmax: float = field(init=False, default=100)
    ymin: float = field(init=False, default=-100)
    ymax: float = field(init=False, default=100)
    n_data: int = field(init=False, default=1000000)
    data: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))

    def generate(self):
        self.n_data = int(self.n_data)
        h_x = (self.xmax - self.xmin) / 2.
        h_y = (self.ymax - self.ymin) / 2.
        n_x = np.random.randint(1, 7)
        n_y = np.random.randint(1, 7)
        p_x, p_y = self.generate_gaussian_2d(h_x, h_y, n_x, n_y, self.n_data)
        p_x = p_x + (self.xmax + self.xmin) / 2.
        p_y = p_y + (self.ymax + self.ymin) / 2.
        self.data = np.array([p_x, p_y]).swapaxes(0, 1)

    def generate_gaussian_2d(
        self,
        half_x: float,
        half_y: float,
        n_x: int,
        n_y: int,
        n_data: int,
        seed: int | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(seed)

        # Peak positions
        if n_x == 1:
            x_peaks = np.array([0])
            sigma_x = half_x / 2
        else:
            x_peaks = np.linspace(- half_x, half_x, n_x)
            sigma_x = half_x / (n_x - 1) / 2

        if n_y == 1:
            y_peaks = np.array([0])
            sigma_y = half_y / 2
        else:
            y_peaks = np.linspace(- half_y, half_y, n_y)
            sigma_y = half_y / (n_y - 1) / 2

        # Select peaks
        peak_indices = rng.integers(0, n_x * n_y, size=n_data)
        ix, iy = divmod(peak_indices, n_y)

        # Generate samples
        x = rng.normal(loc=x_peaks[ix], scale=sigma_x)
        y = rng.normal(loc=y_peaks[iy], scale=sigma_y)

        return x, y


@dataclass
class Hist2dManager:
    xmin: float = field(init=False, default=-100)
    xmax: float = field(init=False, default=100)
    xbin_count: int = field(init=False, default=20)
    ymin: float = field(init=False, default=-100)
    ymax: float = field(init=False, default=100)
    ybin_count: int = field(init=False, default=20)
    zmin: int = field(init=False, default=0)
    zmax: int = field(init=False, default=0)
    title: str = field(init=False, default='')
    label_xaxis: str = field(init=False, default='')
    label_yaxis: str = field(init=False, default='')
    is_zlog: bool = field(init=False, default=False)
    has_colorbar: bool = field(init=False, default=False)
    hist: Hist2dSettings = field(init=False, default_factory=Hist2dSettings)

    def __post_init__(self):
        self.generate_data()

    def generate_data(self):
        self.hist.generate()

    def convert_to_width(self, axis: str):
        if axis == 'x':
            span = self.xmax - self.xmin
            cnt = self.xbin_count
        else:
            span = self.ymax - self.ymin
            cnt = self.ybin_count
        return np.ceil(span / cnt)
