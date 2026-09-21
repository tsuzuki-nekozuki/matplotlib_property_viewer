import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from matplotlib.colors import LogNorm

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSpinBox,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QSplitter, QSizePolicy, QApplication
)

from common.aspect_ratio import AspectRatioWidget
from common.mpl_properties import get_colormap_list
from hist2d.hist2d_manager import Hist2dManager
from hist2d.hist2d_generator import Hist2dCodeGenerator
from hist2d.hist2d_defaults import (ndata_list, default_ndata)


class Hist2dTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # Hist2dManager
        self.h2m = Hist2dManager()
        # Default plot index
        self.xbin_width: float = 0
        self.ybin_width: float = 0
        self.ndata: int = 0

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

        # hist2d with dummy data
        self.text_data_xmin = QLineEdit()
        self.text_data_xmax = QLineEdit()
        self.text_data_ymin = QLineEdit()
        self.text_data_ymax = QLineEdit()
        self.combobox_ndata = QComboBox()
        self.button_generate = QPushButton('Generate')
        self.construct_data_settings()

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

        # title and axis
        self.text_title = QLineEdit()
        self.text_xaxis = QLineEdit()
        self.text_yaxis = QLineEdit()
        self.construct_title_and_axis()

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # x-axis range and binning
        self.spinbox_xmin = QDoubleSpinBox()
        self.spinbox_xmax = QDoubleSpinBox()
        self.spinbox_xbin_count = QSpinBox()
        self.label_xbin_width_value = QLabel()
        self.construct_xsettings()

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # y-axis range and binning
        self.spinbox_ymin = QDoubleSpinBox()
        self.spinbox_ymax = QDoubleSpinBox()
        self.spinbox_ybin_count = QSpinBox()
        self.label_ybin_width_value = QLabel()
        self.construct_ysettings()

        hline4 = QFrame()
        hline4.setFrameShape(QFrame.HLine)
        hline4.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline4)

        # Color map
        self.combobox_colormap = QComboBox()
        self.checkbox_zaxis_logscale = QCheckBox('z-axis log scale')
        self.checkbox_show_colormap = QCheckBox('Show color map')
        self.construct_colormap()

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

    def construct_data_settings(self):
        label_data = QLabel('Data generation range')
        label_data.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_data)

        label_usage = QLabel('Press "Generate" to update data')
        self.layout_options.addWidget(label_usage)

        layout_data1 = QHBoxLayout()
        label_data_xmin = QLabel('x min')
        layout_data1.addWidget(label_data_xmin)
        self.text_data_xmin.setText(str(self.h2m.get_data_param('xmin')))
        layout_data1.addWidget(self.text_data_xmin)
        label_data_xmax = QLabel('x max')
        layout_data1.addWidget(label_data_xmax)
        self.text_data_xmax.setText(str(self.h2m.get_data_param('xmax')))
        layout_data1.addWidget(self.text_data_xmax)
        self.layout_options.addLayout(layout_data1)

        layout_data2 = QHBoxLayout()
        label_data_ymin = QLabel('y min')
        layout_data2.addWidget(label_data_ymin)
        self.text_data_ymin.setText(str(self.h2m.get_data_param('ymin')))
        layout_data2.addWidget(self.text_data_ymin)
        label_data_ymax = QLabel('y max')
        layout_data2.addWidget(label_data_ymax)
        self.text_data_ymax.setText(str(self.h2m.get_data_param('ymax')))
        layout_data2.addWidget(self.text_data_ymax)
        self.layout_options.addLayout(layout_data2)

        layout_data3 = QHBoxLayout()
        label_ndata = QLabel('number of data')
        layout_data3.addWidget(label_ndata)
        self.combobox_ndata.addItems(ndata_list)
        idx = self.combobox_ndata.findText(default_ndata)
        if idx >= 0:
            self.combobox_ndata.setCurrentIndex(idx)
        layout_data3.addWidget(self.combobox_ndata)
        self.button_generate.setFixedWidth(80)
        self.button_generate.clicked.connect(self.on_button_generate_clicked)
        layout_data3.addWidget(self.button_generate)
        self.layout_options.addLayout(layout_data3)

    def on_button_generate_clicked(self):
        try:
            xmin = float(self.text_data_xmin.text())
            xmax = float(self.text_data_xmax.text())
            ymin = float(self.text_data_ymin.text())
            ymax = float(self.text_data_ymax.text())
        except ValueError:
            print('limits should be float.')
        if xmin > xmax:
            print('"xmin" should be small smaller than "xmax".')
            return
        if ymin > ymax:
            print('"ymin" should be small smaller than "ymax".')
            return
        self.h2m.set_data_param('xmin', xmin)
        self.h2m.set_data_param('xmax', xmax)
        self.h2m.set_data_param('ymin', ymin)
        self.h2m.set_data_param('ymax', ymax)

        ndata = self.combobox_ndata.currentText().replace(',', '')
        self.h2m.set_data_param('n', ndata)
        self.h2m.generate_data()
        self.h2m.reset_range()

        self.spinbox_xmin.setMinimum(self.h2m.get_hist_param('xmin'))
        self.spinbox_xmin.setMaximum(self.h2m.get_hist_param('xmax'))
        self.spinbox_xmin.setValue(self.h2m.get_hist_param('xmin'))
        self.spinbox_xmax.setMinimum(self.h2m.get_hist_param('xmin'))
        self.spinbox_xmax.setMaximum(self.h2m.get_hist_param('xmax'))
        self.spinbox_xmax.setValue(self.h2m.get_hist_param('xmax'))
        self.spinbox_ymin.setMinimum(self.h2m.get_hist_param('ymin'))
        self.spinbox_ymin.setMaximum(self.h2m.get_hist_param('ymax'))
        self.spinbox_ymin.setValue(self.h2m.get_hist_param('ymin'))
        self.spinbox_ymax.setMinimum(self.h2m.get_hist_param('ymin'))
        self.spinbox_ymax.setMaximum(self.h2m.get_hist_param('ymax'))
        self.spinbox_ymax.setValue(self.h2m.get_hist_param('ymax'))
        self.update_plot()

    def construct_title_and_axis(self):
        label_title_and_axis = QLabel('Title and Axis')
        label_title_and_axis.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_title_and_axis)

        layout_title = QHBoxLayout()
        label_text_title = QLabel('Title')
        label_text_title.setFixedWidth(50)
        layout_title.addWidget(label_text_title)
        self.text_title.setFixedWidth(240)
        self.text_title.textChanged.connect(self.changed_title)
        layout_title.addWidget(self.text_title)
        self.layout_options.addLayout(layout_title)

        layout_xaxis = QHBoxLayout()
        label_text_xaxis = QLabel('x-axis')
        label_text_xaxis.setFixedWidth(50)
        layout_xaxis.addWidget(label_text_xaxis)
        self.text_xaxis.setFixedWidth(240)
        self.text_xaxis.textChanged.connect(self.changed_xaxis)
        layout_xaxis.addWidget(self.text_xaxis)
        self.layout_options.addLayout(layout_xaxis)

        layout_yaxis = QHBoxLayout()
        label_text_yaxis = QLabel('y-axis')
        label_text_yaxis.setFixedWidth(50)
        layout_yaxis.addWidget(label_text_yaxis)
        self.text_yaxis.setFixedWidth(240)
        self.text_yaxis.textChanged.connect(self.changed_yaxis)
        layout_yaxis.addWidget(self.text_yaxis)
        self.layout_options.addLayout(layout_yaxis)

    def changed_title(self, title):
        self.h2m.set_title_setting('title', title)
        self.update_plot()

    def changed_xaxis(self, xlabel):
        self.h2m.set_title_setting('x', xlabel)
        self.update_plot()

    def changed_yaxis(self, ylabel):
        self.h2m.set_title_setting('y', ylabel)
        self.update_plot()

    def construct_xsettings(self):
        label_xrange = QLabel('x-axis range and binning')
        label_xrange.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_xrange)

        layout_xrange1 = QHBoxLayout()
        label_xmin = QLabel('min')
        layout_xrange1.addWidget(label_xmin)
        self.spinbox_xmin.setFixedWidth(90)
        self.spinbox_xmin.setMinimum(self.h2m.get_hist_param('xmin'))
        self.spinbox_xmin.setMaximum(self.h2m.get_hist_param('xmax'))
        self.spinbox_xmin.setDecimals(2)
        self.spinbox_xmin.setSingleStep(0.01)
        self.spinbox_xmin.setValue(self.h2m.get_hist_param('xmin'))
        self.spinbox_xmin.valueChanged.connect(self.on_spinbox_xmin_changed)
        layout_xrange1.addWidget(self.spinbox_xmin)
        label_xmax = QLabel('max')
        layout_xrange1.addWidget(label_xmax)
        self.spinbox_xmax.setFixedWidth(90)
        self.spinbox_xmax.setMinimum(self.h2m.get_hist_param('xmin'))
        self.spinbox_xmax.setMaximum(self.h2m.get_hist_param('xmax'))
        self.spinbox_xmax.setDecimals(2)
        self.spinbox_xmax.setSingleStep(0.01)
        self.spinbox_xmax.setValue(self.h2m.get_hist_param('xmax'))
        self.spinbox_xmax.valueChanged.connect(self.on_spinbox_xmax_changed)
        layout_xrange1.addWidget(self.spinbox_xmax)
        self.layout_options.addLayout(layout_xrange1)

        layout_xrange2 = QHBoxLayout()
        label_xbin_count = QLabel('bin count')
        layout_xrange2.addWidget(label_xbin_count)
        self.spinbox_xbin_count.setFixedWidth(90)
        self.spinbox_xbin_count.setMinimum(1)
        self.spinbox_xbin_count.setMaximum(100)
        self.spinbox_xbin_count.setSingleStep(1)
        self.spinbox_xbin_count.setValue(self.h2m.get_hist_param('xbin'))
        self.spinbox_xbin_count.valueChanged.connect(
            self.on_spinbox_xbin_count_changed)
        layout_xrange2.addWidget(self.spinbox_xbin_count)

        label_xbin_width = QLabel('bin width: ')
        layout_xrange2.addWidget(label_xbin_width)
        self.label_xbin_width_value.setFixedWidth(90)
        self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        layout_xrange2.addWidget(self.label_xbin_width_value)
        self.layout_options.addLayout(layout_xrange2)

    def on_spinbox_xmin_changed(self, val):
        self.h2m.set_hist_param('xmin', val)
        self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        self.spinbox_xmax.setMinimum(val)
        self.update_plot()

    def on_spinbox_xmax_changed(self, val):
        self.h2m.set_hist_param('xmax', val)
        self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        self.spinbox_xmin.setMaximum(val)
        self.update_plot()

    def on_spinbox_xbin_count_changed(self, val):
        self.h2m.set_hist_param('xbin', val)
        if self.xbin_width is not None:
            self.xbin_width = self.get_xbin_width()
        self.label_xbin_width_value.setText(f'{self.xbin_width:.2f}')
        self.update_plot()

    def get_xbin_width(self):
        xmax = self.h2m.get_hist_param('xmax')
        xmin = self.h2m.get_hist_param('xmin')
        xbin = self.h2m.get_hist_param('xbin')
        return (xmax - xmin) / xbin

    def construct_ysettings(self):
        label_yrange = QLabel('y-axis range and binning')
        label_yrange.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_yrange)

        layout_yrange1 = QHBoxLayout()
        label_ymin = QLabel('min')
        layout_yrange1.addWidget(label_ymin)
        self.spinbox_ymin.setFixedWidth(90)
        self.spinbox_ymin.setMinimum(self.h2m.get_hist_param('ymin'))
        self.spinbox_ymin.setMaximum(self.h2m.get_hist_param('ymax'))
        self.spinbox_ymin.setDecimals(2)
        self.spinbox_ymin.setSingleStep(0.01)
        self.spinbox_ymin.setValue(self.h2m.get_hist_param('ymin'))
        self.spinbox_ymin.valueChanged.connect(self.on_spinbox_ymin_changed)
        layout_yrange1.addWidget(self.spinbox_ymin)
        label_ymax = QLabel('max')
        layout_yrange1.addWidget(label_ymax)
        self.spinbox_ymax.setFixedWidth(90)
        self.spinbox_ymax.setMinimum(self.h2m.get_hist_param('ymin'))
        self.spinbox_ymax.setMaximum(self.h2m.get_hist_param('ymax'))
        self.spinbox_ymax.setDecimals(2)
        self.spinbox_ymax.setSingleStep(0.01)
        self.spinbox_ymax.setValue(self.h2m.get_hist_param('ymax'))
        self.spinbox_ymax.valueChanged.connect(self.on_spinbox_ymax_changed)
        layout_yrange1.addWidget(self.spinbox_ymax)
        self.layout_options.addLayout(layout_yrange1)

        layout_yrange2 = QHBoxLayout()
        label_ybin_count = QLabel('bin count')
        layout_yrange2.addWidget(label_ybin_count)
        self.spinbox_ybin_count.setFixedWidth(90)
        self.spinbox_ybin_count.setMinimum(1)
        self.spinbox_ybin_count.setMaximum(100)
        self.spinbox_ybin_count.setSingleStep(1)
        self.spinbox_ybin_count.setValue(self.h2m.get_hist_param('ybin'))
        self.spinbox_ybin_count.valueChanged.connect(
            self.on_spinbox_ybin_count_changed)
        layout_yrange2.addWidget(self.spinbox_ybin_count)

        label_ybin_width = QLabel('bin width: ')
        layout_yrange2.addWidget(label_ybin_width)
        self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.label_ybin_width_value.setFixedWidth(90)
        layout_yrange2.addWidget(self.label_ybin_width_value)
        self.layout_options.addLayout(layout_yrange2)

    def on_spinbox_ymin_changed(self, val):
        self.h2m.set_hist_param('ymin', val)
        self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.spinbox_ymax.setMinimum(val)
        self.update_plot()

    def on_spinbox_ymax_changed(self, val):
        self.h2m.set_hist_param('ymax', val)
        self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.spinbox_ymin.setMaximum(val)
        self.update_plot()

    def on_spinbox_ybin_count_changed(self, val):
        self.h2m.set_hist_param('ybin', val)
        if self.ybin_width is not None:
            self.ybin_width = self.get_ybin_width()
        self.label_ybin_width_value.setText(f'{self.ybin_width:.2f}')
        self.update_plot()

    def get_ybin_width(self):
        ymax = self.h2m.get_hist_param('ymax')
        ymin = self.h2m.get_hist_param('ymin')
        ybin = self.h2m.get_hist_param('ybin')
        return (ymax - ymin) / ybin

    def construct_colormap(self):
        label_colormap = QLabel('z-axis settings')
        label_colormap.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_colormap)

        layout_colormap = QHBoxLayout()
        label_cmap = QLabel('color map')
        layout_colormap.addWidget(label_cmap)

        colormap = get_colormap_list()
        self.combobox_colormap.addItems(colormap)
        index = self.combobox_colormap.findText(self.h2m.default_colormap)
        if index >= 0:
            self.combobox_colormap.setCurrentIndex(index)
        self.combobox_colormap.currentTextChanged.connect(
            self.on_changed_colormap)
        layout_colormap.addWidget(self.combobox_colormap)
        self.layout_options.addLayout(layout_colormap)

        self.checkbox_zaxis_logscale.stateChanged.connect(self.on_toggle_zaxis)
        self.layout_options.addWidget(self.checkbox_zaxis_logscale)

        self.checkbox_show_colormap.stateChanged.connect(
            self.on_toggle_show_colormap)
        self.layout_options.addWidget(self.checkbox_show_colormap)

    def on_changed_colormap(self, cmap):
        self.h2m.set_colormap(cmap)
        self.update_plot()

    def on_toggle_zaxis(self, state):
        self.h2m.enable_logz(state)
        self.update_plot()

    def on_toggle_show_colormap(self, state):
        self.h2m.enable_colorbar(state)
        self.update_plot()

    def update_plot(self):
        if self.cbar is not None:
            self.cbar.remove()
            self.cbar = None

        self.canvas.ax.axis('on')
        self.canvas.ax.cla()
        if self.h2m.get_logz_state():
            h2 = self.canvas.ax.hist2d(
                self.h2m.get_xdata(), self.h2m.get_ydata(),
                bins=(self.h2m.get_hist_param('xbin'),
                      self.h2m.get_hist_param('ybin')),
                range=((self.h2m.get_hist_param('xmin'),
                        self.h2m.get_hist_param('xmax')),
                       (self.h2m.get_hist_param('ymin'),
                        self.h2m.get_hist_param('ymax'))),
                cmap=self.h2m.get_hist_param('cmap'),
                norm=LogNorm()
            )
        else:
            h2 = self.canvas.ax.hist2d(
                self.h2m.get_xdata(), self.h2m.get_ydata(),
                bins=(self.h2m.get_hist_param('xbin'),
                      self.h2m.get_hist_param('ybin')),
                range=((self.h2m.get_hist_param('xmin'),
                        self.h2m.get_hist_param('xmax')),
                       (self.h2m.get_hist_param('ymin'),
                        self.h2m.get_hist_param('ymax'))),
                cmap=self.h2m.get_hist_param('cmap')
            )
        self.canvas.ax.set_title(self.h2m.get_title_setting('title'))
        self.canvas.ax.set_xlabel(self.h2m.get_title_setting('x'))
        self.canvas.ax.set_ylabel(self.h2m.get_title_setting('y'))
        if self.h2m.get_colorbar_state():
            self.cbar = self.canvas.fig.colorbar(h2[3], ax=self.canvas.ax)
        else:
            self.cbar = None

        self.text_code.setPlainText(self.h2m.generate_code())

        self.canvas.draw()

    def on_button_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_code.toPlainText())
