import matplotlib.pyplot as plt
import numpy as np

from PySide6.QtCore import Qt, QStringListModel, QItemSelectionModel
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSlider,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QStackedWidget, QSplitter, QSizePolicy,
    QApplication
)

from core.mpl_properties import get_colormap_list
from ui.aspect_ratio import AspectRatioWidget


class Hist2dTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # PlotManager
        # self.h2 = Hist2dManager()
        # Default plot index
        self.selected = 0

        # Layout
        self.layout = QHBoxLayout()

        # Splitter
        splitter = QSplitter()

        # canvas
        self.canvas = canvas
        self.ax2 = None
        canvas.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        split_canvas = AspectRatioWidget(canvas, ratio=4/3)
        self.layout.addWidget(split_canvas, alignment=Qt.AlignCenter)

        # options
        split_options = QWidget()
        split_options.setFixedWidth(350)
        self.layout_options = QVBoxLayout(split_options)

        splitter.addWidget(split_canvas)
        splitter.addWidget(split_options)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)

        # hist2d list
        # title and axis
        self.label_title_and_axis = QLabel('Title and Axis')
        self.label_title_and_axis.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_title_and_axis)

        self.layout_title = QHBoxLayout()
        self.label_text_title = QLabel('Title')
        self.label_text_title.setFixedWidth(50)
        self.layout_title.addWidget(self.label_text_title)
        self.text_title = QLineEdit()
        self.text_title.setFixedWidth(240)
        # self.text_title.textChanged.connect(self.changed_title)
        self.layout_title.addWidget(self.text_title)
        self.layout_options.addLayout(self.layout_title)

        self.layout_xaxis = QHBoxLayout()
        self.label_text_xaxis = QLabel('x-axis')
        self.label_text_xaxis.setFixedWidth(50)
        self.layout_xaxis.addWidget(self.label_text_xaxis)
        self.text_xaxis = QLineEdit()
        self.text_xaxis.setFixedWidth(240)
        # self.text_xaxis.textChanged.connect(self.changed_xaxis)
        self.layout_xaxis.addWidget(self.text_xaxis)
        self.layout_options.addLayout(self.layout_xaxis)

        self.layout_yaxis = QHBoxLayout()
        self.label_text_yaxis = QLabel('y-axis')
        self.label_text_yaxis.setFixedWidth(50)
        self.layout_yaxis.addWidget(self.label_text_yaxis)
        self.text_yaxis = QLineEdit()
        self.text_yaxis.setFixedWidth(240)
        # self.text_yaxis.textChanged.connect(self.changed_yaxis)
        self.layout_yaxis.addWidget(self.text_yaxis)
        self.layout_options.addLayout(self.layout_yaxis)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

        # x-axis range and binning
        self.label_xrange = QLabel('x-axis range and binning')
        self.label_xrange.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_xrange)

        self.layout_xrange1 = QHBoxLayout()
        self.label_xmin = QLabel('min')
        self.layout_xrange1.addWidget(self.label_xmin)
        self.spinbox_xmin = QDoubleSpinBox()
        self.spinbox_xmin.setFixedWidth(90)
        self.spinbox_xmin.setMinimum(-100)
        self.spinbox_xmin.setMaximum(100)
        self.spinbox_xmin.setDecimals(2)
        self.spinbox_xmin.setSingleStep(0.01)
        self.spinbox_xmin.setValue(-10)
        self.layout_xrange1.addWidget(self.spinbox_xmin)
        self.label_xmax = QLabel('max')
        self.layout_xrange1.addWidget(self.label_xmax)
        self.spinbox_xmax = QDoubleSpinBox()
        self.spinbox_xmax.setFixedWidth(90)
        self.spinbox_xmax.setMinimum(-100)
        self.spinbox_xmax.setMaximum(100)
        self.spinbox_xmax.setDecimals(2)
        self.spinbox_xmax.setSingleStep(0.01)
        self.spinbox_xmax.setValue(10)
        self.layout_xrange1.addWidget(self.spinbox_xmax)
        self.layout_options.addLayout(self.layout_xrange1)

        self.layout_xrange2 = QHBoxLayout()
        self.label_xbin_width = QLabel('bin width')
        self.layout_xrange2.addWidget(self.label_xbin_width)
        self.spinbox_xbin_width = QDoubleSpinBox()
        self.spinbox_xbin_width.setFixedWidth(90)
        self.spinbox_xbin_width.setMinimum(2)
        self.spinbox_xbin_width.setMaximum(200)
        self.spinbox_xbin_width.setDecimals(1)
        self.spinbox_xbin_width.setSingleStep(0.1)
        self.spinbox_xbin_width.setValue(1)
        self.layout_xrange2.addWidget(self.spinbox_xbin_width)
        self.label_xbin_count = QLabel('bin count')
        self.layout_xrange2.addWidget(self.label_xbin_count)
        self.spinbox_xbin_count = QDoubleSpinBox()
        self.spinbox_xbin_count.setFixedWidth(90)
        self.spinbox_xbin_count.setMinimum(-100)
        self.spinbox_xbin_count.setMaximum(100)
        self.spinbox_xbin_count.setDecimals(0)
        self.spinbox_xbin_count.setSingleStep(0.01)
        self.spinbox_xbin_count.setValue(10)
        self.layout_xrange2.addWidget(self.spinbox_xbin_count)
        self.layout_options.addLayout(self.layout_xrange2)

        self.layout_xrange3 = QVBoxLayout()
        self.radio_group_xbinning = QButtonGroup()
        self.radio_x_keep_range = QRadioButton('Keep bin width')
        self.radio_group_xbinning.addButton(self.radio_x_keep_range)
        self.layout_xrange3.addWidget(self.radio_x_keep_range)
        self.radio_x_adjust = QRadioButton('Fit range explicitly')
        self.radio_group_xbinning.addButton(self.radio_x_adjust)
        self.layout_xrange3.addWidget(self.radio_x_adjust)
        self.layout_options.addLayout(self.layout_xrange3)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # y-axis range and binning
        self.label_yrange = QLabel('y-axis range and binning')
        self.label_yrange.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_yrange)

        self.layout_yrange1 = QHBoxLayout()
        self.label_ymin = QLabel('min')
        self.layout_yrange1.addWidget(self.label_ymin)
        self.spinbox_ymin = QDoubleSpinBox()
        self.spinbox_ymin.setFixedWidth(90)
        self.spinbox_ymin.setMinimum(-100)
        self.spinbox_ymin.setMaximum(100)
        self.spinbox_ymin.setDecimals(2)
        self.spinbox_ymin.setSingleStep(0.01)
        self.spinbox_ymin.setValue(-10)
        self.layout_yrange1.addWidget(self.spinbox_ymin)
        self.label_ymax = QLabel('max')
        self.layout_yrange1.addWidget(self.label_ymax)
        self.spinbox_ymax = QDoubleSpinBox()
        self.spinbox_ymax.setFixedWidth(90)
        self.spinbox_ymax.setMinimum(-100)
        self.spinbox_ymax.setMaximum(100)
        self.spinbox_ymax.setDecimals(2)
        self.spinbox_ymax.setSingleStep(0.01)
        self.spinbox_ymax.setValue(10)
        self.layout_yrange1.addWidget(self.spinbox_ymax)
        self.layout_options.addLayout(self.layout_yrange1)

        self.layout_yrange2 = QHBoxLayout()
        self.label_ybin_width = QLabel('bin width')
        self.layout_yrange2.addWidget(self.label_ybin_width)
        self.spinbox_ybin_width = QDoubleSpinBox()
        self.spinbox_ybin_width.setFixedWidth(90)
        self.spinbox_ybin_width.setMinimum(2)
        self.spinbox_ybin_width.setMaximum(200)
        self.spinbox_ybin_width.setDecimals(1)
        self.spinbox_ybin_width.setSingleStep(0.1)
        self.spinbox_ybin_width.setValue(1)
        self.layout_yrange2.addWidget(self.spinbox_ybin_width)
        self.label_ybin_count = QLabel('bin count')
        self.layout_yrange2.addWidget(self.label_ybin_count)
        self.spinbox_ybin_count = QDoubleSpinBox()
        self.spinbox_ybin_count.setFixedWidth(90)
        self.spinbox_ybin_count.setMinimum(-100)
        self.spinbox_ybin_count.setMaximum(100)
        self.spinbox_ybin_count.setDecimals(0)
        self.spinbox_ybin_count.setSingleStep(0.01)
        self.spinbox_ybin_count.setValue(10)
        self.layout_yrange2.addWidget(self.spinbox_ybin_count)
        self.layout_options.addLayout(self.layout_yrange2)

        self.layout_yrange3 = QVBoxLayout()
        self.radio_group_ybinning = QButtonGroup()
        self.radio_x_keep_range = QRadioButton('Keep bin width')
        self.radio_group_ybinning.addButton(self.radio_x_keep_range)
        self.layout_yrange3.addWidget(self.radio_x_keep_range)
        self.radio_x_adjust = QRadioButton('Fit range explicitly')
        self.radio_group_ybinning.addButton(self.radio_x_adjust)
        self.layout_yrange3.addWidget(self.radio_x_adjust)
        self.layout_options.addLayout(self.layout_yrange3)

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # Color map
        self.label_colormap = QLabel('z-axis settings')
        self.label_colormap.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_colormap)

        self.layout_colormap = QHBoxLayout()
        self.label_cmap = QLabel('color map')
        self.layout_colormap.addWidget(self.label_cmap)

        self.combobox_colormap = QComboBox()
        colormap = get_colormap_list()
        self.combobox_colormap.addItems(colormap)
        index = self.combobox_colormap.findText('viridis')
        if index >= 0:
            self.combobox_colormap.setCurrentIndex(index)
        self.layout_colormap.addWidget(self.combobox_colormap)
        self.layout_options.addLayout(self.layout_colormap)

        self.checkbox_zaxis_logscale = QCheckBox('z-axis log scale')
        # self.checkbox_zaxis_logscale.stateChanged.connect(
        #     self.on_toggle_zaxis)
        self.layout_options.addWidget(self.checkbox_zaxis_logscale)

        self.checkbox_show_colormap = QCheckBox('Show color map')
        # self.checkbox_show_colormap.stateChanged.connect(
        #     self.on_toggle_show_colormap)
        self.layout_options.addWidget(self.checkbox_show_colormap)

        hline4 = QFrame()
        hline4.setFrameShape(QFrame.HLine)
        hline4.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline4)

        # code
        self.label_code = QLabel('Codes')
        self.label_code.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_code)
        self.text_code = QPlainTextEdit()
        self.text_code.setFixedWidth(340)
        self.text_code.setPlainText('This is a text.')
        self.layout_options.addWidget(self.text_code, stretch=1)
        self.button_copy = QPushButton('Copy')
        self.button_copy.setFixedWidth(80)
        # self.button_copy.clicked.connect(self.on_button_copy_clicked)
        self.layout_options.addWidget(
            self.button_copy, alignment=Qt.AlignRight)

        self.layout.addWidget(split_options)
        self.setLayout(self.layout)

        self.update_plot()

    def update_plot(self):
        self.canvas.ax.axis('on')
        self.canvas.ax.cla()

        self.canvas.draw()

    def on_button_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText('hello')
