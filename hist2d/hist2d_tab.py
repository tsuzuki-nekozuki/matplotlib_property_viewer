import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from matplotlib.colors import LogNorm

from PySide6.QtCore import Qt, QStringListModel, QItemSelectionModel
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSlider,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QStackedWidget, QSplitter, QSizePolicy,
    QApplication
)

from common.aspect_ratio import AspectRatioWidget
from common.mpl_properties import get_colormap_list
from hist2d.hist2d_class import Hist2dManager
from hist2d.hist2d_generator import Hist2dCodeGenerator


def is_integer(s: str) -> bool:
    return s.lstrip('-').isdigit()


class Hist2dTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # Hist2dManager
        self.h2m = Hist2dManager()
        # Default plot index
        # self.colormap = plt.rcParams['image.cmap']
        self.xbin_width = None
        self.ybin_width = None
        self.ndata = 0

        # Layout
        self.layout = QHBoxLayout()

        # Splitter
        splitter = QSplitter()

        # canvas
        self.canvas = canvas
        self.cbar = None
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
        # Dummy data
        self.label_data = QLabel('Data range settings')
        self.label_data.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_data)

        self.label_usage = QLabel('Press "Generate" to update data')
        self.layout_options.addWidget(self.label_usage)

        self.layout_data1 = QHBoxLayout()
        self.label_data_xmin = QLabel('x min')
        self.layout_data1.addWidget(self.label_data_xmin)
        self.text_data_xmin = QLineEdit()
        self.text_data_xmin.setText(str(self.h2m.hist.xmin))
        self.layout_data1.addWidget(self.text_data_xmin)
        self.label_data_xmax = QLabel('x max')
        self.layout_data1.addWidget(self.label_data_xmax)
        self.text_data_xmax = QLineEdit()
        self.text_data_xmax.setText(str(self.h2m.hist.xmax))
        self.layout_data1.addWidget(self.text_data_xmax)
        self.layout_options.addLayout(self.layout_data1)

        self.layout_data2 = QHBoxLayout()
        self.label_data_ymin = QLabel('y min')
        self.layout_data2.addWidget(self.label_data_ymin)
        self.text_data_ymin = QLineEdit()
        self.text_data_ymin.setText(str(self.h2m.hist.ymin))
        self.layout_data2.addWidget(self.text_data_ymin)
        self.label_data_ymax = QLabel('y max')
        self.layout_data2.addWidget(self.label_data_ymax)
        self.text_data_ymax = QLineEdit()
        self.text_data_ymax.setText(str(self.h2m.hist.ymax))
        self.layout_data2.addWidget(self.text_data_ymax)
        self.layout_options.addLayout(self.layout_data2)

        self.layout_data3 = QHBoxLayout()
        self.label_ndata = QLabel('number of data')
        self.layout_data3.addWidget(self.label_ndata)
        self.combobox_ndata = QComboBox()
        self.combobox_ndata.addItems(
            [
                '1,000', '2,000', '5,000',
                '10,000', '20,000', '50,000',
                '100,000', '200,000', '500,000',
                '1,000,000', '2,000,000', '5,000,000',
                '10,000,000', '20,000,000', '50,000,000',
                '100,000,000', '200,000,000', '500,000,000'
            ]
        )
        index = self.combobox_ndata.findText('1,000,000')
        if index >= 0:
            self.combobox_ndata.setCurrentIndex(index)
        self.layout_data3.addWidget(self.combobox_ndata)
        self.button_generate = QPushButton('Generate')
        self.button_generate.setFixedWidth(80)
        self.button_generate.clicked.connect(self.on_button_generate_clicked)
        self.layout_data3.addWidget(self.button_generate)
        self.layout_options.addLayout(self.layout_data3)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

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
        self.text_title.textChanged.connect(self.changed_title)
        self.layout_title.addWidget(self.text_title)
        self.layout_options.addLayout(self.layout_title)

        self.layout_xaxis = QHBoxLayout()
        self.label_text_xaxis = QLabel('x-axis')
        self.label_text_xaxis.setFixedWidth(50)
        self.layout_xaxis.addWidget(self.label_text_xaxis)
        self.text_xaxis = QLineEdit()
        self.text_xaxis.setFixedWidth(240)
        self.text_xaxis.textChanged.connect(self.changed_xaxis)
        self.layout_xaxis.addWidget(self.text_xaxis)
        self.layout_options.addLayout(self.layout_xaxis)

        self.layout_yaxis = QHBoxLayout()
        self.label_text_yaxis = QLabel('y-axis')
        self.label_text_yaxis.setFixedWidth(50)
        self.layout_yaxis.addWidget(self.label_text_yaxis)
        self.text_yaxis = QLineEdit()
        self.text_yaxis.setFixedWidth(240)
        self.text_yaxis.textChanged.connect(self.changed_yaxis)
        self.layout_yaxis.addWidget(self.text_yaxis)
        self.layout_options.addLayout(self.layout_yaxis)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # x-axis range and binning
        self.label_xrange = QLabel('x-axis range and binning')
        self.label_xrange.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_xrange)

        self.layout_xrange1 = QHBoxLayout()
        self.label_xmin = QLabel('min')
        self.layout_xrange1.addWidget(self.label_xmin)
        self.spinbox_xmin = QDoubleSpinBox()
        self.spinbox_xmin.setFixedWidth(90)
        self.spinbox_xmin.setMinimum(self.h2m.hist.xmin)
        self.spinbox_xmin.setMaximum(self.h2m.hist.xmax)
        self.spinbox_xmin.setDecimals(2)
        self.spinbox_xmin.setSingleStep(0.01)
        self.spinbox_xmin.setValue(self.h2m.xmin)
        self.spinbox_xmin.valueChanged.connect(self.on_spinbox_xmin_changed)
        self.layout_xrange1.addWidget(self.spinbox_xmin)
        self.label_xmax = QLabel('max')
        self.layout_xrange1.addWidget(self.label_xmax)
        self.spinbox_xmax = QDoubleSpinBox()
        self.spinbox_xmax.setFixedWidth(90)
        self.spinbox_xmax.setMinimum(self.h2m.hist.xmin)
        self.spinbox_xmax.setMaximum(self.h2m.hist.xmax)
        self.spinbox_xmax.setDecimals(2)
        self.spinbox_xmax.setSingleStep(0.01)
        self.spinbox_xmax.setValue(self.h2m.xmax)
        self.spinbox_xmax.valueChanged.connect(self.on_spinbox_xmax_changed)
        self.layout_xrange1.addWidget(self.spinbox_xmax)
        self.layout_options.addLayout(self.layout_xrange1)

        self.layout_xrange2 = QHBoxLayout()
        self.label_xbin_count = QLabel('bin count')
        self.layout_xrange2.addWidget(self.label_xbin_count)
        self.spinbox_xbin_count = QDoubleSpinBox()
        self.spinbox_xbin_count.setFixedWidth(90)
        self.spinbox_xbin_count.setMinimum(1)
        self.spinbox_xbin_count.setMaximum(100)
        self.spinbox_xbin_count.setDecimals(0)
        self.spinbox_xbin_count.setSingleStep(1)
        self.spinbox_xbin_count.setValue(self.h2m.xbin_count)
        self.spinbox_xbin_count.valueChanged.connect(
            self.on_spinbox_xbin_count_changed)
        self.layout_xrange2.addWidget(self.spinbox_xbin_count)

        self.label_xbin_width = QLabel('bin width: ')
        self.layout_xrange2.addWidget(self.label_xbin_width)
        self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value = QLabel(f'{self.xbin_width:.2f}')
        self.label_xbin_width_value.setFixedWidth(90)
        self.layout_xrange2.addWidget(self.label_xbin_width_value)
        self.layout_options.addLayout(self.layout_xrange2)

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # y-axis range and binning
        self.label_yrange = QLabel('y-axis range and binning')
        self.label_yrange.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_yrange)

        self.layout_yrange1 = QHBoxLayout()
        self.label_ymin = QLabel('min')
        self.layout_yrange1.addWidget(self.label_ymin)
        self.spinbox_ymin = QDoubleSpinBox()
        self.spinbox_ymin.setFixedWidth(90)
        self.spinbox_ymin.setMinimum(self.h2m.hist.ymin)
        self.spinbox_ymin.setMaximum(self.h2m.hist.ymax)
        self.spinbox_ymin.setDecimals(2)
        self.spinbox_ymin.setSingleStep(0.01)
        self.spinbox_ymin.setValue(self.h2m.ymin)
        self.spinbox_ymin.valueChanged.connect(self.on_spinbox_ymin_changed)
        self.layout_yrange1.addWidget(self.spinbox_ymin)
        self.label_ymax = QLabel('max')
        self.layout_yrange1.addWidget(self.label_ymax)
        self.spinbox_ymax = QDoubleSpinBox()
        self.spinbox_ymax.setFixedWidth(90)
        self.spinbox_ymax.setMinimum(self.h2m.hist.ymin)
        self.spinbox_ymax.setMaximum(self.h2m.hist.ymax)
        self.spinbox_ymax.setDecimals(2)
        self.spinbox_ymax.setSingleStep(0.01)
        self.spinbox_ymax.setValue(self.h2m.ymax)
        self.spinbox_ymax.valueChanged.connect(self.on_spinbox_ymax_changed)
        self.layout_yrange1.addWidget(self.spinbox_ymax)
        self.layout_options.addLayout(self.layout_yrange1)

        self.layout_yrange2 = QHBoxLayout()
        self.label_ybin_count = QLabel('bin count')
        self.layout_yrange2.addWidget(self.label_ybin_count)
        self.spinbox_ybin_count = QDoubleSpinBox()
        self.spinbox_ybin_count.setFixedWidth(90)
        self.spinbox_ybin_count.setMinimum(1)
        self.spinbox_ybin_count.setMaximum(100)
        self.spinbox_ybin_count.setDecimals(0)
        self.spinbox_ybin_count.setSingleStep(1)
        self.spinbox_ybin_count.setValue(self.h2m.ybin_count)
        self.spinbox_ybin_count.valueChanged.connect(
            self.on_spinbox_ybin_count_changed)
        self.layout_yrange2.addWidget(self.spinbox_ybin_count)

        self.label_ybin_width = QLabel('bin width: ')
        self.layout_yrange2.addWidget(self.label_ybin_width)
        self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value = QLabel(f'{self.ybin_width:.2f}')
        self.label_ybin_width_value.setFixedWidth(90)
        self.layout_yrange2.addWidget(self.label_ybin_width_value)
        self.layout_options.addLayout(self.layout_yrange2)

        hline4 = QFrame()
        hline4.setFrameShape(QFrame.HLine)
        hline4.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline4)

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
        index = self.combobox_colormap.findText(self.h2m.colormap)
        if index >= 0:
            self.combobox_colormap.setCurrentIndex(index)
        self.combobox_colormap.currentTextChanged.connect(
            self.on_changed_colormap)
        self.layout_colormap.addWidget(self.combobox_colormap)
        self.layout_options.addLayout(self.layout_colormap)

        self.checkbox_zaxis_logscale = QCheckBox('z-axis log scale')
        self.checkbox_zaxis_logscale.stateChanged.connect(
            self.on_toggle_zaxis)
        self.layout_options.addWidget(self.checkbox_zaxis_logscale)

        self.checkbox_show_colormap = QCheckBox('Show color map')
        self.checkbox_show_colormap.stateChanged.connect(
            self.on_toggle_show_colormap)
        self.layout_options.addWidget(self.checkbox_show_colormap)

        hline5 = QFrame()
        hline5.setFrameShape(QFrame.HLine)
        hline5.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline5)

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
        self.button_copy.clicked.connect(self.on_button_copy_clicked)
        self.layout_options.addWidget(
            self.button_copy, alignment=Qt.AlignRight)

        self.layout.addWidget(split_options)
        self.setLayout(self.layout)

        self.update_plot()

    def on_button_generate_clicked(self):
        try:
            self.h2m.hist.xmin = float(self.text_data_xmin.text())
        except ValueError:
            print('"xmin" should be float.')
        try:
            self.h2m.hist.xmax = float(self.text_data_xmax.text())
        except ValueError:
            print('"xmax" should be float.')
        try:
            self.h2m.hist.ymin = float(self.text_data_ymin.text())
        except ValueError:
            print('"ymin" should be float.')
        try:
            self.h2m.hist.ymax = float(self.text_data_ymax.text())
        except ValueError:
            print('"ymax" should be float.')
        ndata = self.combobox_ndata.currentText().replace(',', '')
        self.h2m.hist.n_data = int(ndata)
        self.h2m.generate_data()
        self.spinbox_xmin.setMinimum(self.h2m.hist.xmin)
        self.spinbox_xmin.setMaximum(self.h2m.hist.xmax)
        self.spinbox_xmax.setMinimum(self.h2m.hist.xmin)
        self.spinbox_xmax.setMaximum(self.h2m.hist.xmax)
        self.spinbox_ymin.setMinimum(self.h2m.hist.ymin)
        self.spinbox_ymin.setMaximum(self.h2m.hist.ymax)
        self.spinbox_ymax.setMinimum(self.h2m.hist.ymin)
        self.spinbox_ymax.setMaximum(self.h2m.hist.ymax)
        self.update_plot()

    def changed_title(self, title):
        self.h2m.title = title
        self.update_plot()

    def changed_xaxis(self, xlabel):
        self.h2m.label_xaxis = xlabel
        self.update_plot()

    def changed_yaxis(self, ylabel):
        self.h2m.label_yaxis = ylabel
        self.update_plot()

    def on_spinbox_xmin_changed(self, val):
        self.h2m.xmin = val
        self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        self.update_plot()

    def on_spinbox_xmax_changed(self, val):
        self.h2m.xmax = val
        self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        self.update_plot()

    def on_spinbox_xbin_count_changed(self, val):
        self.h2m.xbin_count = int(val)
        if self.xbin_width is not None:
            self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        self.update_plot()

    def get_xbin_width(self):
        return (self.h2m.xmax - self.h2m.xmin) / self.h2m.xbin_count

    def on_spinbox_ymin_changed(self, val):
        self.h2m.ymin = val
        self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.update_plot()

    def on_spinbox_ymax_changed(self, val):
        self.h2m.ymax = val
        self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.update_plot()

    def on_spinbox_ybin_count_changed(self, val):
        self.h2m.ybin_count = int(val)
        if self.ybin_width is not None:
            self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.update_plot()

    def get_ybin_width(self):
        return (self.h2m.ymax - self.h2m.ymin) / self.h2m.ybin_count

    def on_changed_colormap(self, cmap):
        self.h2m.colormap = cmap
        self.update_plot()

    def on_toggle_zaxis(self, state):
        self.h2m.is_zlog = state
        self.update_plot()

    def on_toggle_show_colormap(self, state):
        self.h2m.has_colorbar = state
        self.update_plot()

    def update_plot(self):
        if self.cbar is not None:
            self.cbar.remove()
            self.cbar = None

        self.canvas.ax.axis('on')
        self.canvas.ax.cla()
        if self.h2m.is_zlog:
            h2 = self.canvas.ax.hist2d(
                self.h2m.hist.data[:, 0], self.h2m.hist.data[:, 1],
                bins=(self.h2m.xbin_count, self.h2m.ybin_count),
                range=((self.h2m.xmin, self.h2m.xmax),
                       (self.h2m.ymin, self.h2m.ymax)),
                cmap=self.h2m.colormap,
                norm=LogNorm())
        else:
            h2 = self.canvas.ax.hist2d(
                self.h2m.hist.data[:, 0], self.h2m.hist.data[:, 1],
                bins=(self.h2m.xbin_count, self.h2m.ybin_count),
                range=(
                    (self.h2m.xmin, self.h2m.xmax),
                    (self.h2m.ymin, self.h2m.ymax)
                ),
                cmap=self.h2m.colormap)
        self.canvas.ax.set_title(self.h2m.title)
        self.canvas.ax.set_xlabel(self.h2m.label_xaxis)
        self.canvas.ax.set_ylabel(self.h2m.label_yaxis)
        if self.h2m.has_colorbar:
            self.cbar = self.canvas.fig.colorbar(h2[3], ax=self.canvas.ax)
        else:
            self.cbar = None

        code = Hist2dCodeGenerator()
        self.text_code.setPlainText(code.generate(self.h2m))

        self.canvas.draw()

    def on_button_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_code.toPlainText())
