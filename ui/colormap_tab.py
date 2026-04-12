import matplotlib.pyplot as plt
import numpy as np

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSlider, QLabel,
    QDoubleSpinBox, QLineEdit, QPushButton
)

from core.mpl_properties import get_colormap_list


class ColormapTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        self.layout_colormap = QVBoxLayout()

        # canvas
        self.canvas = canvas
        self.layout_colormap.addWidget(self.canvas)

        self.label_colormap = QLabel('color map')
        self.layout_colormap.addWidget(self.label_colormap)

        self.combobox_colormap = QComboBox()
        colormap = get_colormap_list()
        self.combobox_colormap.addItems(colormap)
        index = self.combobox_colormap.findText('viridis')
        if index >= 0:
            self.combobox_colormap.setCurrentIndex(index)
        self.layout_colormap.addWidget(self.combobox_colormap)

        self.draw_button = QPushButton('Draw')
        self.draw_button.clicked.connect(self.on_draw_button)
        self.layout_colormap.addWidget(self.draw_button)

        self.setLayout(self.layout_colormap)

        # initial plot
        self.update_plot()

    def on_draw_button(self):
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        self.canvas.ax.imshow(
            gradient, aspect='auto', cmap=self.combobox_colormap.currentText())
        self.canvas.ax.axis('off')
        self.canvas.draw()

    def update_plot(self):
        self.canvas.ax.axis('off')
        self.canvas.draw()
