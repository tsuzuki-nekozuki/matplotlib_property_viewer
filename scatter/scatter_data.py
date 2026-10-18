from dataclasses import dataclass, field

import numpy as np

from numpy.typing import NDArray


@dataclass
class OneScatterData:
    ndata: int = field(init=True)
    xmin: float = field(init=True)
    xmax: float = field(init=True)
    ymin: float = field(init=True)
    ymax: float = field(init=True)
    zmin: float = field(init=True)
    zmax: float = field(init=True)
    x: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))
    y: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))
    z: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))

    def __post_init__(self):
        self.generate()

    def generate(self, is_random: bool = True):
        if is_random:
            self.x = np.random.uniform(self.xmin, self.xmax, self.ndata)
            self.y = np.random.uniform(self.ymin, self.ymax, self.ndata)
            self.z = np.random.uniform(self.zmin, self.zmax, self.ndata)


@dataclass
class ScatterData:
    data: list[OneScatterData] = field(init=False, default_factory=list)
    xmin: float = field(init=False, default=-50)
    xmax: float = field(init=False, default=50)
    ymin: float = field(init=False, default=-50)
    ymax: float = field(init=False, default=50)
    zmin: float = field(init=False, default=0)
    zmax: float = field(init=False, default=10)
    ndata: int = field(init=False, default=3)

    def generate(self):
        self.data = []
        size = 100
        for _ in range(self.ndata):
            d = OneScatterData(
                size,
                self.xmin, self.xmax,
                self.ymin, self.ymax,
                self.zmin, self.zmax
            )
            d.generate()
            self.data.append(d)

    def get_data(self, idx: int, axis: None | str = None):
        if axis is None:
            return self.data[idx]
        elif axis == 'x':
            return self.data[idx].x
        elif axis == 'y':
            return self.data[idx].y
        elif axis == 'z':
            return self.data[idx].z
        else:
            raise ValueError(f'Unknown axis: {axis}')
