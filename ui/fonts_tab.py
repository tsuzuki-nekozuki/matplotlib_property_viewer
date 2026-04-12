import matplotlib.pyplot as plt
import numpy as np

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSlider, QLabel,
    QDoubleSpinBox, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

from core.mpl_properties import get_fonts_list, get_color_list


class FontsTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        self.layout_fonts = QVBoxLayout()

        # canvas
        self.canvas = canvas
        self.layout_fonts.addWidget(self.canvas)

        # style
        self.layout_style = QVBoxLayout()

        self.label_style = QLabel('style')
        self.layout_style.addWidget(self.label_style)

        self.combobox_fonts = QComboBox()
        style_list = get_fonts_list()
        self.combobox_fonts.addItems(style_list)
        self.layout_style.addWidget(self.combobox_fonts)

        # color
        self.layout_color = QVBoxLayout()

        self.label_color = QLabel('named colors')
        self.layout_color.addWidget(self.label_color)

        self.combobox_fonts_color = QComboBox()
        fonts_color = get_color_list()
        self.combobox_fonts_color.addItems(fonts_color)
        for i, icolor in enumerate(fonts_color):
            if icolor.startswith('- '):
                self.combobox_fonts_color.model().item(i).setEnabled(False)
        self.layout_color.addWidget(self.combobox_fonts_color)

        # fonts style and color
        self.layout_fonts1 = QHBoxLayout()
        self.layout_fonts1.addLayout(self.layout_style)
        self.layout_fonts1.addLayout(self.layout_color)

        # fonts size
        self.layout_fonts_size = QHBoxLayout()

        self.value = 7
        self.slider_value = self.value * 10
        self.slider_fonts_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_fonts_size.setMinimum(1)
        self.slider_fonts_size.setMaximum(300)
        self.slider_fonts_size.setValue(self.slider_value)
        self.layout_fonts_size.addWidget(self.slider_fonts_size)

        self.spinbox_fonts_size = QDoubleSpinBox()
        self.spinbox_fonts_size.setMinimum(0.1)
        self.spinbox_fonts_size.setMaximum(30)
        self.spinbox_fonts_size.setDecimals(1)
        self.spinbox_fonts_size.setSingleStep(0.1)
        self.spinbox_fonts_size.setValue(self.value)
        self.layout_fonts_size.addWidget(self.spinbox_fonts_size)

        self.layout_fonts2 = QVBoxLayout()
        self.label_fonts_size = QLabel('size')
        self.layout_fonts2.addWidget(self.label_fonts_size)
        self.layout_fonts2.addLayout(self.layout_fonts_size)

        # add fonts layouts
        self.label_fonts_title = QLabel('Fonts')
        self.label_fonts_title.setStyleSheet('font-size: 18px;')
        self.layout_fonts.addWidget(self.label_fonts_title)
        self.layout_fonts.addLayout(self.layout_fonts1)
        self.layout_fonts.addLayout(self.layout_fonts2)

        self.draw_button = QPushButton('Draw')
        self.layout_fonts.addWidget(self.draw_button)

        self.setLayout(self.layout_fonts)

        # initial plot
        self.update_plot()

    def on_slider_change(self):
        self.update_plot()

    def update_plot(self):
        self.canvas.ax.axis('off')

        self.canvas.draw()
