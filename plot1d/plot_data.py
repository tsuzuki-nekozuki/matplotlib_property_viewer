from dataclasses import dataclass, field

import numpy as np

from numpy.typing import NDArray


@dataclass
class OnePlotData:
    x: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))
    y: NDArray[np.float64] = field(
        init=False, default_factory=lambda: np.empty(0, dtype=np.float64))

    def generate(self, is_random: bool = True, offset: float = 0):
        if is_random:
            self.generate_random(offset)

    def generate_random(self, offset: float = 0):
        self.x = np.arange(100)
        self.y = np.random.rand(100) + (offset + 1)


@dataclass
class PlotData:
    data: list = field(init=False, default_factory=list)

    def __post_init__(self):
        self.add_data(is_random=True, offset=0)

    def add_data(self, is_random: bool, offset: float):
        one_data = OnePlotData()
        one_data.generate(is_random, offset)
        self.data.append(one_data)

    def delete_data(self):
        del self.data[-1]

    def get_plot_data(self, idx: int):
        return self.data[idx]
