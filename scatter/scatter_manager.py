import matplotlib.pyplot as plt
import numpy as np

from numpy.typing import NDArray

from scatter.scatter_data import ScatterData
from scatter.scatter_settings import ScatterSettings, OneScatterSettings


class ScatterManager:
    def __init__(self):
        self.n_scatter: int = 3
        self.data = ScatterData()
        self.settings = ScatterSettings()

    def generate_data(self):
        self.settings.set_nplots(self.data.ndata)
        self.data.generate()
        for i in range(self.data.ndata):
            self.settings.plots[i].scatter_type = 'scatter'

    def set_title_setting(self, item: str, value: str):
        match item:
            case 'title':
                self.settings.title = str(value)
            case 'x':
                self.settings.label_xaxis = str(value)
            case 'y':
                self.settings.label_yaxis = str(value)
            case _:
                raise ValueError(f'Unknown hist2d setting: {item}')

    def get_title_setting(self, item: str):
        match item:
            case 'title':
                return self.settings.title
            case 'x':
                return self.settings.label_xaxis
            case 'y':
                return self.settings.label_yaxis
            case _:
                raise ValueError(f'Unknown hist2d setting: {item}')

    def set_data_param(self, param: str, value: float | int | str):
        min_max_check = True
        match param:
            case 'xmin':
                if float(value) < self.data.xmax:
                    self.data.xmin = float(value)
                else:
                    min_max_check = False
            case 'xmax':
                if float(value) > self.data.xmin:
                    self.data.xmax = float(value)
                else:
                    min_max_check = False
            case 'ymin':
                if float(value) < self.data.ymax:
                    self.data.ymin = float(value)
                else:
                    min_max_check = False
            case 'ymax':
                if float(value) > self.data.ymin:
                    self.data.ymax = float(value)
                else:
                    min_max_check = False
            case 'zmin':
                if float(value) <= 0:
                    min_max_check = False
                elif float(value) < self.data.zmax:
                    self.data.zmin = float(value)
                else:
                    min_max_check = False
            case 'zmax':
                if float(value) > self.data.zmin:
                    self.data.zmax = float(value)
                else:
                    min_max_check = False
            case _:
                raise ValueError(f'Unknown scatter setting: {param}')
        if not min_max_check:
            return False
        return True

    def get_data_param(self, param: str) -> float:
        match param:
            case 'xmin':
                return self.data.xmin
            case 'xmax':
                return self.data.xmax
            case 'ymin':
                return self.data.ymin
            case 'ymax':
                return self.data.ymax
            case 'zmin':
                return self.data.zmin
            case 'zmax':
                return self.data.zmax
            case _:
                raise ValueError(f'Unknown scatter setting: {param}')

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
                self.settings.is_ylog = state
            case _:
                raise ValueError(f'Unknown plot setting: {axis}')

    def get_logscale_state(self, axis: str):
        match axis:
            case 'x':
                return self.settings.is_xlog
            case 'y':
                return self.settings.is_ylog
            case _:
                raise ValueError(f'Unknown plot setting: {axis}')
