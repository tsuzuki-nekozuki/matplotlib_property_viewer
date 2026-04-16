import sys
import matplotlib.pyplot as plt
import numpy as np

from PySide6.QtCore import Qt, QStringListModel, QItemSelectionModel
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSlider,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QStackedWidget, QSplitter, QSizePolicy
)

from core.mpl_properties import get_color_list, get_marker_list, get_line_list
from core.plot_class import PlotManager
from ui.aspect_ratio import AspectRatioWidget


class PlotTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # PlotManager
        self.pm = PlotManager()
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

        # plots list
        self.layout_plots_list = QVBoxLayout()

        self.layout_plots_list_title = QHBoxLayout()
        self.label_plots_list = QLabel(
            f'Plots list (max: {self.pm.max_nplots})')
        self.label_plots_list.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_plots_list)

        self.layout_plots_list = QHBoxLayout()
        self.list_plots = QStringListModel()
        self.list_plots.setStringList(self.pm.plot_names)
        self.list_plots.dataChanged.connect(self.on_update_plots_list)
        self.view_plots = QListView()
        self.view_plots.setFlow(QListView.Flow.TopToBottom)
        self.view_plots.setWrapping(True)
        self.view_plots.setResizeMode(QListView.ResizeMode.Adjust)
        self.view_plots.setModel(self.list_plots)
        idx = self.list_plots.index(0, 0)
        self.view_plots.selectionModel().setCurrentIndex(
            idx, QItemSelectionModel.ClearAndSelect)
        self.view_plots.setFixedSize(240, 120)
        self.view_plots.selectionModel().currentChanged.connect(
            self.on_view_plots_selected)
        self.layout_plots_list.addWidget(self.view_plots)

        self.layout_plots_buttons = QVBoxLayout()
        self.button_add = QPushButton('Add')
        self.button_add.setFixedWidth(80)
        self.button_add.clicked.connect(self.on_button_add_clicked)
        self.layout_plots_buttons.addWidget(self.button_add)
        self.button_delete = QPushButton('Delete')
        self.button_delete.setFixedWidth(80)
        self.button_delete.clicked.connect(self.on_button_delete_clicked)
        self.layout_plots_buttons.addWidget(self.button_delete)
        self.checkbox_2axes = QCheckBox('2axes')
        self.checkbox_2axes.stateChanged.connect(self.on_toggle_2axes)
        self.layout_plots_buttons.addWidget(self.checkbox_2axes)

        self.layout_plots_list.addLayout(self.layout_plots_buttons)
        self.layout_options.addLayout(self.layout_plots_list)
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

        self.layout_plot_setting = QVBoxLayout()
        self.layout_grid_axes = QHBoxLayout()
        self.checkbox_grid = QCheckBox('add grid')
        self.checkbox_grid.stateChanged.connect(self.on_toggle_grid)
        self.layout_grid_axes.addWidget(self.checkbox_grid)
        self.checkbox_xaxis_logscale = QCheckBox('x-axis log scale')
        self.checkbox_xaxis_logscale.stateChanged.connect(self.on_toggle_xaxis)
        self.layout_grid_axes.addWidget(self.checkbox_xaxis_logscale)
        self.checkbox_yaxis_logscale = QCheckBox('y-axis1 log scale')
        self.checkbox_yaxis_logscale.stateChanged.connect(self.on_toggle_yaxis)
        self.layout_grid_axes.addWidget(self.checkbox_yaxis_logscale)
        self.layout_plot_setting.addLayout(self.layout_grid_axes)

        self.layout_radio_2axes = QHBoxLayout()
        self.radio_group_axis = QButtonGroup()
        self.stack_radio_axis1 = QStackedWidget()
        self.empty1 = QWidget()
        self.stack_radio_axis1.addWidget(self.empty1)
        self.radio_axis1 = QRadioButton('axis1')
        self.radio_group_axis.addButton(self.radio_axis1)
        self.stack_radio_axis1.addWidget(self.radio_axis1)
        self.layout_radio_2axes.addWidget(self.stack_radio_axis1)
        self.stack_radio_axis2 = QStackedWidget()
        self.empty2 = QWidget()
        self.stack_radio_axis2.addWidget(self.empty2)
        self.radio_axis2 = QRadioButton('axis2')
        self.radio_group_axis.addButton(self.radio_axis2)
        self.stack_radio_axis2.addWidget(self.radio_axis2)
        self.layout_radio_2axes.addWidget(self.stack_radio_axis2)
        self.radio_axis1.clicked.connect(self.on_radio_clicked_2axes)
        self.radio_axis2.clicked.connect(self.on_radio_clicked_2axes)
        self.radio_axis1.setVisible(False)
        self.radio_axis2.setVisible(False)
        self.checkbox_yaxis2_logscale = QCheckBox('y-axis2 log scale')
        self.checkbox_yaxis2_logscale.setVisible(False)
        self.checkbox_yaxis2_logscale.stateChanged.connect(
            self.on_toggle_yaxis2)
        self.layout_radio_2axes.addWidget(self.checkbox_yaxis2_logscale)
        self.layout_plot_setting.addLayout(self.layout_radio_2axes)
        self.layout_options.addLayout(self.layout_plot_setting)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # marker
        self.label_marker = QLabel('Marker')
        self.label_marker.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_marker)

        self.layout_marker1 = QHBoxLayout()

        self.label_marker_style = QLabel('style')
        self.layout_marker1.addWidget(self.label_marker_style)

        self.combobox_marker_style = QComboBox()
        marker_styles = get_marker_list()
        self.combobox_marker_style.addItems(marker_styles)
        self.combobox_marker_style.currentTextChanged.connect(
            self.on_changed_marker_style)
        self.layout_marker1.addWidget(self.combobox_marker_style)

        self.label_marker_color = QLabel('color')
        self.layout_marker1.addWidget(self.label_marker_color)

        self.combobox_marker_color = QComboBox()
        colors = get_color_list()
        self.combobox_marker_color.addItems(colors)
        for i, icolor in enumerate(colors):
            if icolor.startswith('- '):
                self.combobox_marker_color.model().item(i).setEnabled(False)
        index = self.combobox_marker_color.findText(
            self.pm.plots[self.selected].marker_color)
        if index >= 0:
            self.combobox_marker_color.setCurrentIndex(index)
        self.combobox_marker_color.currentTextChanged.connect(
            self.on_changed_marker_color)
        self.layout_marker1.addWidget(self.combobox_marker_color)

        self.layout_marker2 = QHBoxLayout()
        self.label_marker_size = QLabel('size')
        self.layout_marker2.addWidget(self.label_marker_size)
        self.layout_options.addLayout(self.layout_marker1)

        self.marker_size = self.pm.plots[self.selected].marker_size
        self.marker_size2 = self.marker_size * 10
        self.slider_marker_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_marker_size.setFixedWidth(210)
        self.slider_marker_size.setMinimum(1)
        self.slider_marker_size.setMaximum(150)
        self.slider_marker_size.setValue(self.marker_size2)
        self.slider_marker_size.valueChanged.connect(
            self.on_slider_marker_size_changed)
        self.layout_marker2.addWidget(self.slider_marker_size)

        self.spinbox_marker_size = QDoubleSpinBox()
        self.spinbox_marker_size.setFixedWidth(60)
        self.spinbox_marker_size.setMinimum(0.1)
        self.spinbox_marker_size.setMaximum(15)
        self.spinbox_marker_size.setDecimals(1)
        self.spinbox_marker_size.setSingleStep(0.1)
        self.spinbox_marker_size.setValue(self.marker_size)
        self.spinbox_marker_size.valueChanged.connect(
            self.on_spinbox_marker_size_changed)
        self.layout_marker2.addWidget(self.spinbox_marker_size)
        self.layout_options.addLayout(self.layout_marker2)

        # line
        self.label_line = QLabel('Line')
        self.label_line.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_line)

        self.layout_line1 = QHBoxLayout()

        self.label_line_style = QLabel('style')
        self.layout_line1.addWidget(self.label_line_style)

        self.combobox_line_style = QComboBox()
        styles = get_line_list()
        self.combobox_line_style.addItems(styles)
        index = self.combobox_line_style.findText(
            self.pm.plots[self.selected].line_style)
        if index >= 0:
            self.combobox_line_style.setCurrentIndex(index)
        self.combobox_line_style.currentTextChanged.connect(
            self.on_changed_line_style)
        self.layout_line1.addWidget(self.combobox_line_style)

        self.label_line_color = QLabel('color')
        self.layout_line1.addWidget(self.label_line_color)

        self.combobox_line_color = QComboBox()
        self.combobox_line_color.addItems(colors)
        for i, icolor in enumerate(colors):
            if icolor.startswith('- '):
                self.combobox_line_color.model().item(i).setEnabled(False)
        index = self.combobox_line_color.findText(
            self.pm.plots[self.selected].line_color)
        if index >= 0:
            self.combobox_line_color.setCurrentIndex(index)
        self.combobox_line_color.currentTextChanged.connect(
            self.on_changed_line_color)
        self.layout_line1.addWidget(self.combobox_line_color)
        self.layout_options.addLayout(self.layout_line1)

        self.layout_line2 = QHBoxLayout()
        self.label_line_width = QLabel('width')
        self.layout_line2.addWidget(self.label_line_width)

        self.line_width = self.pm.plots[self.selected].line_width
        self.line_width2 = self.line_width * 10
        self.slider_line_width = QSlider(Qt.Orientation.Horizontal)
        self.slider_line_width.setFixedWidth(210)
        self.slider_line_width.setMinimum(1)
        self.slider_line_width.setMaximum(50)
        self.slider_line_width.setValue(self.line_width2)
        self.slider_line_width.valueChanged.connect(
            self.on_slider_line_width_changed)
        self.layout_line2.addWidget(self.slider_line_width)

        self.spinbox_line_width = QDoubleSpinBox()
        self.spinbox_line_width.setFixedWidth(60)
        self.spinbox_line_width.setMinimum(0.1)
        self.spinbox_line_width.setMaximum(5)
        self.spinbox_line_width.setDecimals(1)
        self.spinbox_line_width.setSingleStep(0.1)
        self.spinbox_line_width.setValue(self.line_width)
        self.spinbox_line_width.valueChanged.connect(
            self.on_spinbox_line_width_changed)
        self.layout_line2.addWidget(self.spinbox_line_width)
        self.layout_options.addLayout(self.layout_line2)
        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # code
        self.label_code = QLabel('Codes')
        self.label_code.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_code)
        self.text_code = QPlainTextEdit()
        self.text_code.setFixedWidth(340)
        self.text_code.setPlainText('This is a text.')
        self.layout_options.addWidget(self.text_code, stretch=1)

        # layouts
        self.layout.addWidget(split_options)
        self.setLayout(self.layout)

        # initial plot
        self.update_plot()

    def update_view_plots(self):
        self.list_plots.setStringList(self.pm.plot_names)
        self.view_plots.setModel(self.list_plots)
        self.update_plot()

    def on_view_plots_selected(self, current):
        self.selected = current.row()
        self.set_current_values(self.pm.plots[self.selected])

    def set_current_values(self, plot):
        if self.pm.has_twin_axes:
            if plot.yaxis == 0:
                self.radio_axis1.setChecked(True)
                self.radio_axis2.setChecked(False)
            else:
                self.radio_axis1.setChecked(False)
                self.radio_axis2.setChecked(True)
        idx = self.combobox_marker_style.findText(plot.marker_style)
        if idx >= 0:
            self.combobox_marker_style.setCurrentIndex(idx)
        idx = self.combobox_marker_color.findText(plot.marker_color)
        if idx >= 0:
            self.combobox_marker_color.setCurrentIndex(idx)
        self.slider_marker_size.setValue(plot.marker_size * 10)
        self.spinbox_marker_size.setValue(plot.marker_size)
        idx = self.combobox_line_style.findText(plot.line_style)
        if idx >= 0:
            self.combobox_line_style.setCurrentIndex(idx)
        idx = self.combobox_line_color.findText(plot.line_color)
        if idx >= 0:
            self.combobox_line_color.setCurrentIndex(idx)
        self.slider_line_width.setValue(plot.line_width * 10)
        self.spinbox_line_width.setValue(plot.line_width)

    def on_button_add_clicked(self):
        if not self.pm.add_plot():
            return
        self.update_view_plots()
        # Select new plot
        idx = self.list_plots.index(self.pm.nplots - 1, 0)
        self.view_plots.selectionModel().setCurrentIndex(
            idx, QItemSelectionModel.ClearAndSelect)

    def on_button_delete_clicked(self):
        # Get current selected plot
        idx = self.view_plots.selectionModel().currentIndex()
        current_row = idx.row()
        if not self.pm.delete_plot():
            return
        self.update_view_plots()
        # Select current plot; if deleted select the last plot
        if current_row >= self.pm.nplots:
            current_row = self.pm.nplots - 1
        idx = self.list_plots.index(current_row, 0)
        self.view_plots.selectionModel().setCurrentIndex(
            idx, QItemSelectionModel.ClearAndSelect)

    def on_update_plots_list(self, first):
        idx = first.row()
        new_plot_name = self.list_plots.data(first)
        self.pm.plot_names[idx] = new_plot_name
        self.update_view_plots()

    def changed_title(self, title):
        self.pm.title = title
        self.update_plot()

    def changed_xaxis(self, xlabel):
        self.pm.label_xaxis = xlabel
        self.update_plot()

    def changed_yaxis(self, ylabel):
        self.pm.label_yaxis = ylabel
        self.update_plot()

    def on_toggle_grid(self, state):
        self.pm.has_grid = state
        self.update_plot()

    def on_toggle_xaxis(self, state):
        self.pm.is_xlog = state
        self.update_plot()

    def on_toggle_yaxis(self, state):
        self.pm.is_y1log = state
        self.update_plot()

    def on_toggle_yaxis2(self, state):
        self.pm.is_y2log = state
        self.update_plot()

    def on_toggle_2axes(self, state):
        self.pm.has_twin_axes = state
        self.stack_radio_axis1.setCurrentIndex(1 if state else 0)
        self.stack_radio_axis2.setCurrentIndex(1 if state else 0)
        self.radio_axis1.setChecked(True)
        self.checkbox_yaxis2_logscale.setVisible(state)
        self.checkbox_yaxis2_logscale.setChecked(False)

    def on_radio_clicked_2axes(self):
        if self.radio_axis1.isChecked():
            self.pm.plots[self.selected].yaxis = 0
        elif self.radio_axis2.isChecked():
            self.pm.plots[self.selected].yaxis = 1
        self.update_plot()

    def on_changed_marker_style(self, style):
        self.pm.plots[self.selected].marker_style = style
        self.update_plot()

    def on_changed_marker_color(self, color):
        self.pm.plots[self.selected].marker_color = color
        self.update_plot()

    def on_slider_marker_size_changed(self, val):
        self.marker_size2 = val
        self.marker_size = val / 10
        self.spinbox_marker_size.blockSignals(True)
        self.spinbox_marker_size.setValue(self.marker_size)
        self.spinbox_marker_size.blockSignals(False)
        self.pm.plots[self.selected].marker_size = self.marker_size
        self.update_plot()

    def on_spinbox_marker_size_changed(self, val):
        self.marker_size = val
        self.marker_size2 = val * 10
        self.slider_marker_size.blockSignals(True)
        self.slider_marker_size.setValue(self.marker_size2)
        self.slider_marker_size.blockSignals(False)
        self.pm.plots[self.selected].marker_size = self.marker_size
        self.update_plot()

    def on_changed_line_style(self, style):
        self.pm.plots[self.selected].line_style = style
        self.update_plot()

    def on_changed_line_color(self, color):
        self.pm.plots[self.selected].line_color = color
        self.update_plot()

    def on_slider_line_width_changed(self, val):
        self.line_width2 = val
        self.line_width = val / 10
        self.spinbox_line_width.blockSignals(True)
        self.spinbox_line_width.setValue(self.line_width)
        self.spinbox_line_width.blockSignals(False)
        self.pm.plots[self.selected].line_width = self.line_width
        self.update_plot()

    def on_spinbox_line_width_changed(self, val):
        self.line_width = val
        self.line_width2 = val * 10
        self.slider_line_width.blockSignals(True)
        self.slider_line_width.setValue(self.line_width2)
        self.slider_line_width.blockSignals(False)
        self.pm.plots[self.selected].line_width = self.line_width
        self.update_plot()

    def update_plot(self):
        self.pm.normalize()
        self.canvas.ax.axis('on')
        self.canvas.ax.cla()
        if self.pm.need_two_axes():
            if self.ax2 is None:
                self.ax2 = self.canvas.ax.twinx()
            else:
                self.ax2.cla()
        else:
            if self.ax2 is not None:
                self.ax2.remove()
                self.ax2 = None
        self.canvas.ax.grid(self.pm.has_grid)
        self.canvas.ax.set_title(self.pm.title)
        self.canvas.ax.set_xlabel(self.pm.label_xaxis)
        self.canvas.ax.set_ylabel(self.pm.label_yaxis)

        xscale = 'log' if self.pm.is_xlog else 'linear'
        self.canvas.ax.set_xscale(xscale)
        yscale1 = 'log' if self.pm.is_y1log else 'linear'
        self.canvas.ax.set_yscale(yscale1)
        if self.pm.need_two_axes():
            yscale2 = 'log' if self.pm.is_y2log else 'linear'
            self.ax2.set_yscale(yscale2)
            for ip in self.pm.plots:
                ax = self.canvas.ax if ip.yaxis == 0 else self.ax2
                ax.plot(ip.x, ip.y, **ip.plot_kwargs())
        else:
            self.ax2 = None
            for ip in self.pm.plots:
                self.canvas.ax.plot(ip.x, ip.y, **ip.plot_kwargs())

        self.canvas.draw()
