import sys
import matplotlib.pyplot as plt
import numpy as np

from PySide6.QtCore import Qt, QStringListModel, QItemSelectionModel
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSlider,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QStackedWidget, QSplitter, QSizePolicy,
    QApplication, QGroupBox, QGridLayout
)

from core.mpl_properties import get_fonts_list, get_color_list, get_line_list, get_marker_list
from core.plot_class import PlotManager
from core.plot_generator import CodeGenerator
from ui.aspect_ratio import AspectRatioWidget


class FontsTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # text
        self.text_data = 'write your text here.'
        self.pm = PlotManager()
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

        # text
        self.label_text = QLabel('Text')
        self.label_text.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_text)

        self.text_edit = QLineEdit()
        # self.text_edit.setFixedWidth(350)
        self.text_edit.setText(self.text_data)
        self.text_edit.textChanged.connect(self.changed_text)
        self.layout_options.addWidget(self.text_edit)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

        self.label_settings = QLabel('Settings')
        self.label_settings.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_settings)
        self.layout_font = QHBoxLayout()
        self.label_font = QLabel('font')
        self.layout_font.addWidget(self.label_font)
        self.combobox_font = QComboBox()
        style_list = get_fonts_list()
        self.combobox_font.addItems(style_list)
        self.layout_font.addWidget(self.combobox_font)
        self.layout_options.addLayout(self.layout_font)

        # size and weight
        self.layout_size_weight = QHBoxLayout()
        self.label_size = QLabel('Size')
        self.layout_size_weight.addWidget(self.label_size)

        self.spinbox_size = QDoubleSpinBox()
        self.spinbox_size.setFixedWidth(90)
        self.spinbox_size.setMinimum(0.1)
        self.spinbox_size.setMaximum(50)
        self.spinbox_size.setDecimals(1)
        self.spinbox_size.setSingleStep(0.1)
        self.spinbox_size.setValue(15)
        # self.spinbox_size.valueChanged.connect(self.on_size_changed)
        self.layout_size_weight.addWidget(self.spinbox_size)

        self.label_weight = QLabel('Weight')
        self.layout_size_weight.addWidget(self.label_weight)

        self.spinbox_weight = QDoubleSpinBox()
        self.spinbox_weight.setFixedWidth(90)
        self.spinbox_weight.setMinimum(1)
        self.spinbox_weight.setMaximum(50)
        self.spinbox_weight.setDecimals(1)
        self.spinbox_weight.setSingleStep(0.1)
        self.spinbox_weight.setValue(15)
        # self.spinbox_weight.valueChanged.connect(self.on_weight_changed)
        self.layout_size_weight.addWidget(self.spinbox_weight)
        self.layout_options.addLayout(self.layout_size_weight)

        # color
        font_color = get_color_list()
        self.layout_color1 = QHBoxLayout()
        self.label_color1 = QLabel('foreground color')
        self.layout_color1.addWidget(self.label_color1)
        self.combobox_color1 = QComboBox()
        self.combobox_color1.setFixedWidth(200)
        self.combobox_color1.addItems(font_color)
        for i, icolor in enumerate(font_color):
            if icolor.startswith('- '):
                self.combobox_color1.model().item(i).setEnabled(False)
        self.layout_color1.addWidget(self.combobox_color1)
        self.layout_options.addLayout(self.layout_color1)

        self.layout_color2 = QHBoxLayout()
        self.label_color2 = QLabel('background color')
        self.layout_color2.addWidget(self.label_color2)
        self.combobox_color2 = QComboBox()
        self.combobox_color2.setFixedWidth(200)
        self.combobox_color2.addItems(font_color)
        for i, icolor in enumerate(font_color):
            if icolor.startswith('- '):
                self.combobox_color2.model().item(i).setEnabled(False)
        self.layout_color2.addWidget(self.combobox_color2)
        self.layout_options.addLayout(self.layout_color2)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # target
        self.label_size = QLabel('Target')
        self.label_size.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_size)
        FONT_TARGETS = {
            'Figure': [
                ('Figure Title', 'suptitle'),
            ],
            'Axes': [
                ('Title', 'title'),
                ('X Label', 'xlabel'),
                ('Y Label', 'ylabel'),
                ('X Tick Labels', 'xtick'),
                ('Y Tick Labels', 'ytick'),
            ],
            'Other': [
                ('Legend', 'legend'),
                ('Colorbar', 'colorbar'),
                ('Text', 'text'),
                ('Annotation', 'annotation'),
            ],
        }

        self.layout_target = QGridLayout()
        self.layout_target.setVerticalSpacing(2)
        self.layout_target.setHorizontalSpacing(10)
        self.button_group = QButtonGroup(self)
        self.button_to_key = {}
        self.buttons = {}
        row = 0
        for category, targets in FONT_TARGETS.items():
            category_label = QLabel(category)
            self.layout_target.addWidget(category_label, row, 0)
            for i, (label, key) in enumerate(targets):
                button = QRadioButton(label)

                self.button_group.addButton(button)
                self.button_to_key[button] = key
                self.buttons[key] = button

                self.layout_target.addWidget(button, row + i, 1)
            row += len(targets)
        self.layout_options.addLayout(self.layout_target)
        self.buttons["suptitle"].setChecked(True)
        self.button_group.buttonClicked.connect(self.on_target_changed)

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
        self.button_copy = QPushButton('Copy')
        self.button_copy.setFixedWidth(80)
        self.button_copy.clicked.connect(self.on_button_copy_clicked)
        self.layout_options.addWidget(
            self.button_copy, alignment=Qt.AlignRight)

        # layouts
        self.layout.addWidget(split_options)
        self.setLayout(self.layout)

        # initial plot
        self.update_plot()

    def changed_text(self, text):
        self.text = text
        self.update_plot()

    def on_button_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_code.toPlainText())

    def on_target_changed(self, button):
        key = self.button_to_key[button]
        print(f'target = {key}')

    def update_plot(self):
        self.canvas.ax.axis('off')

        self.canvas.draw()
