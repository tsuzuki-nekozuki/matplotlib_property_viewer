from dataclasses import dataclass
from typing import ClassVar
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.font_manager import FontProperties
from numpy.typing import NDArray


@dataclass
class FontsSettings:
    target: str = field(init=False, default='suptitle')
    font: str = field(init=False, default=plt.rcParams['font.family'][0])
    style: str = field(init=False, default=plt.rcParams['font.style'])
    size: float | str = field(
        init=False, default=plt.rcParams['figure.titlesize'])
    weight: int = field(
        init=False, default=plt.rcParams['figure.titleweight'])
    foreground: str = field(
        init=False, default=plt.rcParams['text.color'])
    background: str = field(init=False, default='none')


@dataclass
class FontsManager:
    user_settings: FontsSettings = field(
        init=False, default_factory=FontsSettings)
    default_rcparams: ClassVar[dict[str, dict[str, str | None]]] = {
        'suptitle': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['figure.titlesize'],
            'Weight': plt.rcParams['figure.titleweight'],
            'Foreground Color': plt.rcParams['text.color'],
            'Background Color': 'none',
        },
        'title': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['axes.titlesize'],
            'Weight': plt.rcParams['axes.titleweight'],
            'Foreground Color': plt.rcParams['axes.titlecolor'],
            'Background Color': 'none',
        },
        'xlabel': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['axes.labelsize'],
            'Weight': plt.rcParams['axes.labelweight'],
            'Foreground Color': plt.rcParams['axes.labelcolor'],
            'Background Color': 'none',
        },
        'ylabel': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['axes.labelsize'],
            'Weight': plt.rcParams['axes.labelweight'],
            'Foreground Color': plt.rcParams['axes.labelcolor'],
            'Background Color': 'none',
        },
        'xtick': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['xtick.labelsize'],
            'Weight': plt.rcParams['font.weight'],
            'Foreground Color': plt.rcParams['xtick.color'],
            'Background Color': 'none',
        },
        'ytick': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['ytick.labelsize'],
            'Weight': plt.rcParams['font.weight'],
            'Foreground Color': plt.rcParams['ytick.color'],
            'Background Color': 'none',
        },
        'legend': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['legend.fontsize'],
            'Weight': plt.rcParams['font.weight'],
            'Foreground Color': plt.rcParams['text.color'],
            'Background Color': plt.rcParams['legend.facecolor'],
        },
        'colorbar': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['xtick.labelsize'],
            'Weight': plt.rcParams['font.weight'],
            'Foreground Color': plt.rcParams['xtick.color'],
            'Background Color': plt.rcParams['axes.facecolor'],
        },
        'text': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['font.size'],
            'Weight': plt.rcParams['font.weight'],
            'Foreground Color': plt.rcParams['text.color'],
            'Background Color': 'none',
        },
        'annotation': {
            'Font Family': plt.rcParams['font.family'][0],
            'Font Style': plt.rcParams['font.style'],
            'Size': plt.rcParams['font.size'],
            'Weight': plt.rcParams['font.weight'],
            'Foreground Color': plt.rcParams['text.color'],
            'Background Color': 'none',
        },
    }

    def __post_init__(self):
        for k, v in self.default_rcparams.items():
            if isinstance(v['Size'], str):
                v['Size'] = self.get_font_size_value(v['Size'])

    def get_font_size_value(self, font_size):
        return FontProperties(font_size).get_size_in_points()

    def get_default_settings(self) -> dict:
        return self.default_rcparams[self.target]

    @property
    def default_font(self) -> str:
        return self.default_rcparams[self.target]['Font Family']

    @property
    def default_style(self) -> str:
        return self.default_rcparams[self.target]['Font Style']

    @property
    def default_size(self) -> float:
        return self.default_rcparams[self.target]['Size']

    @property
    def default_weight(self) -> float:
        return self.default_rcparams[self.target]['Weight']

    @property
    def default_foreground(self) -> str:
        return self.default_rcparams[self.target]['Foreground Color']

    @property
    def default_background(self) -> str:
        return self.default_rcparams[self.target]['Background Color']

    @property
    def target(self) -> str:
        return self.user_settings.target

    @target.setter
    def target(self, value: str):
        self.user_settings.target = value

    @property
    def font(self) -> str:
        return self.user_settings.font

    @font.setter
    def font(self, value: str):
        self.user_settings.font = value

    @property
    def style(self) -> str:
        return self.user_settings.style

    @style.setter
    def style(self, value: str):
        self.user_settings.style = value

    @property
    def size(self) -> float:
        return self.user_settings.size

    @size.setter
    def size(self, value: float):
        self.user_settings.size = value

    @property
    def weight(self) -> str:
        return self.user_settings.weight

    @weight.setter
    def weight(self, value: str):
        self.user_settings.weight = value

    @property
    def foreground(self) -> str:
        return self.user_settings.foreground

    @foreground.setter
    def foreground(self, value: str):
        self.user_settings.foreground = value

    @property
    def background(self) -> str:
        return self.user_settings.background

    @background.setter
    def background(self, value: str):
        self.user_settings.background = value
