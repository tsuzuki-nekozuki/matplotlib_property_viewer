from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np

from numpy.typing import NDArray

from hist2d.hist2d_data import Hist2dData
from hist2d.hist2d_defaults import default_cmap
from hist2d.hist2d_generator import Hist2dCodeGenerator
from hist2d.hist2d_settings import Hist2dSettings


class Hist2dManager:
    def __init__(self):
        self.default_colormap: str = default_cmap
        self.data: Hist2dData = Hist2dData()
        self.settings: Hist2dSettings = Hist2dSettings()
        self.code: Hist2dCodeGenerator = Hist2dCodeGenerator(self.settings)

    def generate_data(self):
        self.data.generate()

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
        match param:
            case 'xmin':
                self.data.xmin = float(value)
            case 'xmax':
                self.data.xmax = float(value)
            case 'ymin':
                self.data.ymin = float(value)
            case 'ymax':
                self.data.ymax = float(value)
            case 'n':
                self.data.ndata = int(value)
            case _:
                raise ValueError(f'Unknown hist2d setting: {param}')

    def get_data_param(self, param: str):
        match param:
            case 'xmin':
                return self.data.xmin
            case 'xmax':
                return self.data.xmax
            case 'ymin':
                return self.data.ymin
            case 'ymax':
                return self.data.ymax
            case 'n':
                return self.data.ndata
            case _:
                raise ValueError(f'Unknown hist2d setting: {param}')

    def set_hist_param(self, param: str, value: float | int | str):
        match param:
            case 'xmin':
                self.settings.xmin = float(value)
            case 'xmax':
                self.settings.xmax = float(value)
            case 'xbin':
                self.settings.xbin_count = int(value)
            case 'ymin':
                self.settings.ymin = float(value)
            case 'ymax':
                self.settings.ymax = float(value)
            case 'ybin':
                self.settings.ybin_count = int(value)
            case 'cmap':
                self.settings.colormap = str(value)
            case _:
                raise ValueError(f'Unknown hist2d setting: {param}')

    def get_hist_param(self, param: str):
        match param:
            case 'xmin':
                return self.settings.xmin
            case 'xmax':
                return self.settings.xmax
            case 'xbin':
                return self.settings.xbin_count
            case 'ymin':
                return self.settings.ymin
            case 'ymax':
                return self.settings.ymax
            case 'ybin':
                return self.settings.ybin_count
            case 'cmap':
                return self.settings.colormap
            case _:
                raise ValueError(f'Unknown hist2d setting: {param}')

    def reset_range(self):
        self.settings.xmin = self.data.xmin
        self.settings.xmax = self.data.xmax
        self.settings.ymin = self.data.ymin
        self.settings.ymax = self.data.ymax

    def enable_logz(self, state: bool):
        self.settings.is_zlog = state

    def get_logz_state(self):
        return self.settings.is_zlog

    def set_colormap(self, cmap: str):
        self.settings.colormap = cmap

    def get_colormap(self):
        return self.settings.colormap

    def enable_colorbar(self, state: bool):
        self.settings.has_colorbar = state

    def get_colorbar_state(self):
        return self.settings.has_colorbar

    def get_xdata(self):
        return self.data.data[:, 0]

    def get_ydata(self):
        return self.data.data[:, 1]

    def generate_code(self):
        return self.code.generate()
