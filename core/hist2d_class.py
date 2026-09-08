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
    colormap: str = field(init=False, default=plt.rcParams['image.cmap'])
    data: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))

    def __post_init__(self):
        self.data = self.generate(
            self.xmin, self.xmax, self.ymin, self.ymax, self.n_data)

    def generate(
        self,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
        n_data: int
    ):
        n_data = int(n_data)
        half_x = (x_max - x_min) / 2.
        half_y = (y_max - y_min) / 2.
        n_x = np.random.randint(1, 7)
        n_y = np.random.randint(1, 7)
        p_x, p_y = self.generate_gaussian_2d(half_x, half_y, n_x, n_y, n_data)
        p_x = p_x - (x_max + x_min) / 2.
        p_y = p_y - (y_max + y_min) / 2.
        return np.array([p_x, p_y]).swapaxes(0, 1)

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
    # colormap: str = field(init=False, default=plt.rcParams['image.cmap'])
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

    def generate_data(self, n: int = 1000000):
        self.hist.generate(self.xmin, self.xmax, self.ymin, self.ymax, n)
    
    @property
    def colormap(self) -> str:
        return self.hist.colormap

    @colormap.setter
    def colormap(self, value: str):
        self.hist.colormap = value
