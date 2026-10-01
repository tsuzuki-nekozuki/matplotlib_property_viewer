import matplotlib.pyplot as plt

from PySide6.QtCore import Qt, QStringListModel, QItemSelectionModel
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSlider,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QStackedWidget, QSplitter, QSizePolicy,
    QApplication, QGridLayout
)

from common.aspect_ratio import AspectRatioWidget
from common.mpl_properties import (
    get_color_list, get_marker_list, get_line_list, get_colormap_list
)


class ScatterTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

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

        # data range
        self.spinbox_xmin = QDoubleSpinBox()
        self.spinbox_xmax = QDoubleSpinBox()
        self.spinbox_ymin = QDoubleSpinBox()
        self.spinbox_ymax = QDoubleSpinBox()
        self.construct_data_range()

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

        # scatter list
        self.text_data = []
        self.button_group_types = QButtonGroup(self)
        self.button_group_color_types = QButtonGroup(self)
        self.data_list = []
        for i in range(3):
            self.data_list.append(f'data{i + 1}')
            self.text_data.append(QLineEdit())
        # self.construct_scatters_list()

        # title and axis
        self.text_title = QLineEdit()
        self.text_xaxis = QLineEdit()
        self.text_yaxis = QLineEdit()
        self.checkbox_grid = QCheckBox('add grid')
        self.checkbox_xaxis_logscale = QCheckBox('x-axis log scale')
        self.checkbox_yaxis_logscale = QCheckBox('y-axis1 log scale')
        self.radio_group_axis = QButtonGroup()
        self.stack_radio_axis1 = QStackedWidget()
        self.radio_axis1 = QRadioButton('axis1')
        self.stack_radio_axis2 = QStackedWidget()
        self.radio_axis2 = QRadioButton('axis2')
        self.checkbox_yaxis2_logscale = QCheckBox('y-axis2 log scale')
        self.construct_title_and_axis()

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # scatter options
        self.combobox_data = QComboBox()
        self.combobox_marker_style = QComboBox()
        self.marker_alpha = 10
        self.spinbox_marker_alpha = QDoubleSpinBox()
        self.marker_size = 10
        self.combobox_marker_color1 = QComboBox()
        self.spinbox_marker_size = QDoubleSpinBox()
        self.marker_width = 1
        self.combobox_marker_color2 = QComboBox()
        self.spinbox_marker_width = QDoubleSpinBox()
        self.combobox_colormap = QComboBox()
        self.spinbox_vmin = QDoubleSpinBox()
        self.spinbox_vmax = QDoubleSpinBox()
        self.construct_scatter_options()

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # Disable / Enable
        self.set_color_settings()

        # code
        label_code = QLabel('Codes')
        label_code.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_code)
        self.text_code = QPlainTextEdit()
        self.text_code.setFixedWidth(340)
        self.text_code.setPlainText('This is a text.')
        self.layout_options.addWidget(self.text_code, stretch=1)
        self.button_copy = QPushButton('Copy')
        self.button_copy.setFixedWidth(80)
        # self.button_copy.clicked.connect(self.on_button_copy_clicked)
        self.layout_options.addWidget(
            self.button_copy, alignment=Qt.AlignRight)

        # layouts
        self.layout.addWidget(split_options)
        self.setLayout(self.layout)

        # initial plot
        # self.update_plot()

    def construct_data_range(self):
        label_range = QLabel('Data range (size: 100)')
        label_range.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_range)

        layout_range1 = QHBoxLayout()
        label_xmin = QLabel('xmin')
        layout_range1.addWidget(label_xmin)
        self.spinbox_xmin.setFixedWidth(90)
        self.spinbox_xmin.setMinimum(-50)
        self.spinbox_xmin.setMaximum(50)
        self.spinbox_xmin.setDecimals(2)
        self.spinbox_xmin.setSingleStep(0.01)
        self.spinbox_xmin.setValue(-50)
        # self.spinbox_xmin.valueChanged.connect(self.on_spinbox_xmin_changed)
        layout_range1.addWidget(self.spinbox_xmin)
        label_xmax = QLabel('xmax')
        layout_range1.addWidget(label_xmax)
        self.spinbox_xmax.setFixedWidth(90)
        self.spinbox_xmax.setMinimum(-50)
        self.spinbox_xmax.setMaximum(50)
        self.spinbox_xmax.setDecimals(2)
        self.spinbox_xmax.setSingleStep(0.01)
        self.spinbox_xmax.setValue(50)
        # self.spinbox_xmax.valueChanged.connect(self.on_spinbox_xmax_changed)
        layout_range1.addWidget(self.spinbox_xmax)
        self.layout_options.addLayout(layout_range1)

        layout_range2 = QHBoxLayout()
        label_ymin = QLabel('ymin')
        layout_range2.addWidget(label_ymin)
        self.spinbox_ymin.setFixedWidth(90)
        self.spinbox_ymin.setMinimum(-50)
        self.spinbox_ymin.setMaximum(50)
        self.spinbox_ymin.setDecimals(2)
        self.spinbox_ymin.setSingleStep(0.01)
        self.spinbox_ymin.setValue(-50)
        # self.spinbox_ymin.valueChanged.connect(self.on_spinbox_ymin_changed)
        layout_range2.addWidget(self.spinbox_ymin)
        label_ymax = QLabel('ymax')
        layout_range2.addWidget(label_ymax)
        self.spinbox_ymax.setFixedWidth(90)
        self.spinbox_ymax.setMinimum(-50)
        self.spinbox_ymax.setMaximum(50)
        self.spinbox_ymax.setDecimals(2)
        self.spinbox_ymax.setSingleStep(0.01)
        self.spinbox_ymax.setValue(50)
        # self.spinbox_ymax.valueChanged.connect(self.on_spinbox_ymax_changed)
        layout_range2.addWidget(self.spinbox_ymax)
        self.layout_options.addLayout(layout_range2)

    def construct_title_and_axis(self):
        label_title_and_axis = QLabel('Title and Axis')
        label_title_and_axis.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_title_and_axis)

        layout_title = QHBoxLayout()
        label_text_title = QLabel('Title')
        label_text_title.setFixedWidth(50)
        layout_title.addWidget(label_text_title)
        self.text_title.setFixedWidth(240)
        # self.text_title.textChanged.connect(self.changed_title)
        layout_title.addWidget(self.text_title)
        self.layout_options.addLayout(layout_title)

        layout_xaxis = QHBoxLayout()
        label_text_xaxis = QLabel('x-axis')
        label_text_xaxis.setFixedWidth(50)
        layout_xaxis.addWidget(label_text_xaxis)
        self.text_xaxis.setFixedWidth(240)
        # self.text_xaxis.textChanged.connect(self.changed_xaxis)
        layout_xaxis.addWidget(self.text_xaxis)
        self.layout_options.addLayout(layout_xaxis)

        layout_yaxis = QHBoxLayout()
        label_text_yaxis = QLabel('y-axis')
        label_text_yaxis.setFixedWidth(50)
        layout_yaxis.addWidget(label_text_yaxis)
        self.text_yaxis.setFixedWidth(240)
        # self.text_yaxis.textChanged.connect(self.changed_yaxis)
        layout_yaxis.addWidget(self.text_yaxis)
        self.layout_options.addLayout(layout_yaxis)

        layout_plot_setting = QVBoxLayout()
        layout_grid_axes = QHBoxLayout()
        # self.checkbox_grid.stateChanged.connect(self.on_toggle_grid)
        layout_grid_axes.addWidget(self.checkbox_grid)
        # self.checkbox_xaxis_logscale.stateChanged.connect(self.on_toggle_xaxis)
        layout_grid_axes.addWidget(self.checkbox_xaxis_logscale)
        # self.checkbox_yaxis_logscale.stateChanged.connect(self.on_toggle_yaxis)
        layout_grid_axes.addWidget(self.checkbox_yaxis_logscale)
        layout_plot_setting.addLayout(layout_grid_axes)
        self.layout_options.addLayout(layout_plot_setting)

    def construct_scatter_options(self):
        self.construct_types_selection()
        self.construct_marker()

    def construct_types_selection(self):
        label_scatter_options = QLabel('Settings')
        label_scatter_options.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_scatter_options)

        layout_data = QHBoxLayout()
        label_selected = QLabel('Selected data')
        layout_data.addWidget(label_selected)
        self.combobox_data.addItems(self.data_list)
        # self.combobox_data.currentTextChanged.connect(self.on_changed_data)
        layout_data.addWidget(self.combobox_data)
        self.layout_options.addLayout(layout_data)

        layout_data = QHBoxLayout()
        label_data = QLabel('Plot name')
        label_data.setFixedWidth(90)
        layout_data.addWidget(label_data)
        layout_data.addWidget(self.text_data[0])
        self.layout_options.addLayout(layout_data)

        types = ['scatter', 'bubble', 'off']
        layout_types = QGridLayout()
        label_types = QLabel('Plot type')
        label_types.setFixedWidth(90)
        layout_types.addWidget(label_types, 0, 1)
        for i, itype in enumerate(types):
            button = QRadioButton(itype)
            self.button_group_types.addButton(button, id=i)
            layout_types.addWidget(button, 0, i + 2)
        self.button_group_types.button(0).setChecked(True)
        self.layout_options.addLayout(layout_types)

        color_types = ['solid color', 'colormap']
        layout_color_types = QGridLayout()
        label_color_types = QLabel('Color type')
        label_color_types.setFixedWidth(90)
        layout_color_types.addWidget(label_color_types, 0, 1)
        for i, itype in enumerate(color_types):
            button = QRadioButton(itype)
            self.button_group_color_types.addButton(button, id=i)
            layout_color_types.addWidget(button, 0, i + 2)
        self.button_group_color_types.button(0).setChecked(True)
        self.layout_options.addLayout(layout_color_types)
        label_attention = QLabel(
            'Note: Common color setting, if "colormap" is selected.')
        label_attention.setStyleSheet('font-size: 10px;')
        self.layout_options.addWidget(label_attention, alignment=Qt.AlignRight)

    def construct_marker(self):
        label_marker = QLabel('Marker')
        label_marker.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_marker)

        layout_marker1 = QHBoxLayout()

        label_marker_style = QLabel('style')
        layout_marker1.addWidget(label_marker_style)
        marker_styles = get_marker_list()
        self.combobox_marker_style.setFixedWidth(120)
        self.combobox_marker_style.addItems(marker_styles)
        # self.combobox_marker_style.currentTextChanged.connect(
        #     self.on_changed_marker_style)
        layout_marker1.addWidget(self.combobox_marker_style)

        label_marker_alpha = QLabel('alpha')
        layout_marker1.addWidget(label_marker_alpha)
        self.spinbox_marker_alpha.setFixedWidth(90)
        self.spinbox_marker_alpha.setMinimum(0)
        self.spinbox_marker_alpha.setMaximum(1)
        self.spinbox_marker_alpha.setValue(self.marker_alpha)
        # self.spinbox_marker_alpha.valueChanged.connect(
        #     self.on_slider_marker_alpha_changed)
        layout_marker1.addWidget(self.spinbox_marker_alpha)
        self.layout_options.addLayout(layout_marker1)

        layout_marker2 = QHBoxLayout()
        label_marker_color1 = QLabel('color')
        layout_marker2.addWidget(label_marker_color1)

        colors = get_color_list()
        self.combobox_marker_color1.setFixedWidth(120)
        self.combobox_marker_color1.addItems(colors)
        for i, icolor in enumerate(colors):
            if icolor.startswith('- '):
                self.combobox_marker_color1.model().item(i).setEnabled(False)
        self.combobox_marker_color1.setCurrentIndex(0)
        # self.combobox_marker_color1.currentTextChanged.connect(
        #     self.on_changed_marker_color1)
        layout_marker2.addWidget(self.combobox_marker_color1)

        label_marker_size = QLabel('size')
        layout_marker2.addWidget(label_marker_size)

        self.spinbox_marker_size.setFixedWidth(90)
        self.spinbox_marker_size.setMinimum(1)
        self.spinbox_marker_size.setMaximum(150)
        self.spinbox_marker_size.setValue(self.marker_size)
        # self.spinbox_marker_size.valueChanged.connect(
        #     self.on_spinbox_marker_size_changed)
        layout_marker2.addWidget(self.spinbox_marker_size)
        self.layout_options.addLayout(layout_marker2)

        layout_marker3 = QHBoxLayout()
        label_marker_color2 = QLabel('edge')
        layout_marker3.addWidget(label_marker_color2)

        colors = get_color_list()
        self.combobox_marker_color2.setFixedWidth(120)
        self.combobox_marker_color2.addItems(colors)
        for i, icolor in enumerate(colors):
            if icolor.startswith('- '):
                self.combobox_marker_color2.model().item(i).setEnabled(False)
        self.combobox_marker_color2.setCurrentIndex(0)
        # self.combobox_marker_color2.currentTextChanged.connect(
        #     self.on_changed_marker_color2)
        layout_marker3.addWidget(self.combobox_marker_color2)

        label_marker_width = QLabel('width')
        layout_marker3.addWidget(label_marker_width)

        self.spinbox_marker_width.setFixedWidth(90)
        self.spinbox_marker_width.setMinimum(1)
        self.spinbox_marker_width.setMaximum(150)
        self.spinbox_marker_width.setValue(self.marker_width)
        # self.spinbox_marker_width.valueChanged.connect(
        #     self.on_spinbox_marker_width_changed)
        layout_marker3.addWidget(self.spinbox_marker_width)
        self.layout_options.addLayout(layout_marker3)

        layout_marker4 = QHBoxLayout()
        label_marker_colormap = QLabel('colormap')
        layout_marker4.addWidget(label_marker_colormap)

        colormap = get_colormap_list()
        self.combobox_colormap.addItems(colormap)
        index = self.combobox_colormap.findText('viridis')
        if index >= 0:
            self.combobox_colormap.setCurrentIndex(index)
        # self.combobox_colormap.currentTextChanged.connect(
        #     self.on_changed_colormap)
        layout_marker4.addWidget(self.combobox_colormap)
        self.layout_options.addLayout(layout_marker4)

        layout_marker5 = QHBoxLayout()
        label_vmin = QLabel('vmin')
        layout_marker5.addWidget(label_vmin)
        self.spinbox_vmin.setFixedWidth(90)
        self.spinbox_vmin.setMinimum(0)
        self.spinbox_vmin.setMaximum(1)
        self.spinbox_vmin.setDecimals(2)
        self.spinbox_vmin.setSingleStep(0.01)
        self.spinbox_vmin.setValue(0)
        # self.spinbox_vmin.valueChanged.connect(self.on_spinbox_vmin_changed)
        layout_marker5.addWidget(self.spinbox_vmin)
        label_vmax = QLabel('vmax')
        layout_marker5.addWidget(label_vmax)
        self.spinbox_vmax.setFixedWidth(90)
        self.spinbox_vmax.setMinimum(0)
        self.spinbox_vmax.setMaximum(1)
        self.spinbox_vmax.setDecimals(2)
        self.spinbox_vmax.setSingleStep(0.01)
        self.spinbox_vmax.setValue(1)
        # self.spinbox_vmax.valueChanged.connect(self.on_spinbox_vmax_changed)
        layout_marker5.addWidget(self.spinbox_vmax)
        self.layout_options.addLayout(layout_marker5)

    def set_color_settings(self):
        if self.button_group_color_types.checkedId() == 0:  # solid
            self.combobox_colormap.setEnabled(False)
            self.spinbox_vmin.setEnabled(False)
            self.spinbox_vmax.setEnabled(False)
            self.combobox_marker_color1.setEnabled(True)
        elif self.button_group_color_types.checkedId() == 1:  # colormap
            self.combobox_colormap.setEnabled(True)
            self.spinbox_vmin.setEnabled(True)
            self.spinbox_vmax.setEnabled(True)
            self.combobox_marker_color1.setEnabled(False)
